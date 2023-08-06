# -*- coding: utf-8 -*-

"""Main module."""

import configparser
import gc
import json
import logging
import multiprocessing
import os
# import shelve
import shutil
from datetime import datetime
from queue import Empty
from subprocess import PIPE, TimeoutExpired
# import time
from urllib.parse import urljoin
from uuid import uuid4

import mutagen.id3
import pkg_resources
import youtube_dl
from boltons.urlutils import find_all_links, URL
from botanio import botan
from plumbum import local
from pydub import AudioSegment
from pyshorteners import Shortener
from telegram import MessageEntity, ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultAudio
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

logger = logging.getLogger(__name__)


class SCDLBot:
    MAX_TG_FILE_SIZE = 45000000
    SITES = {
        "sc": "soundcloud",
        "scapi": "api.soundcloud",
        "bc": "bandcamp",
        "yt": "youtu",
    }

    def __init__(self, tg_bot_token, botan_token=None, google_shortener_api_key=None, bin_path="",
                 sc_auth_token=None, store_chat_id=None, no_clutter_chat_ids=None,
                 alert_chat_ids=None, dl_dir="/tmp/scdl", dl_timeout=3600, max_convert_file_size=500000000):
        self.DL_TIMEOUT = dl_timeout
        self.MAX_CONVERT_FILE_SIZE = max_convert_file_size
        self.HELP_TEXT = self.get_response_text('help.tg.md')
        self.DL_TIMEOUT_TEXT = self.get_response_text('dl_timeout.txt').format(self.DL_TIMEOUT // 60)
        self.WAIT_TEXT = self.get_response_text('wait.txt')
        self.NO_AUDIO_TEXT = self.get_response_text('no_audio.txt')
        self.NO_URLS_TEXT = self.get_response_text('no_urls.txt')
        self.REGION_RESTRICTION_TEXT = self.get_response_text('region_restriction.txt')
        self.DIRECT_RESTRICTION_TEXT = self.get_response_text('direct_restriction.txt')
        self.LIVE_RESTRICTION_TEXT = self.get_response_text('live_restriction.txt')
        self.NO_CLUTTER_CHAT_IDS = set(no_clutter_chat_ids) if no_clutter_chat_ids else set()
        self.ALERT_CHAT_IDS = set(alert_chat_ids) if alert_chat_ids else set()
        self.STORE_CHAT_ID = store_chat_id
        self.DL_DIR = dl_dir
        self.scdl = local[os.path.join(bin_path, 'scdl')]
        self.bandcamp_dl = local[os.path.join(bin_path, 'bandcamp-dl')]
        self.youtube_dl = local[os.path.join(bin_path, 'youtube-dl')]
        self.botan_token = botan_token if botan_token else None
        self.shortener = Shortener('Google', api_key=google_shortener_api_key) if google_shortener_api_key else None
        self.msg_store = {}
        self.rant_msg_ids = {}

        config = configparser.ConfigParser()
        config['scdl'] = {}
        config['scdl']['path'] = self.DL_DIR
        if sc_auth_token:
            config['scdl']['auth_token'] = sc_auth_token
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'scdl')
        config_path = os.path.join(config_dir, 'scdl.cfg')
        os.makedirs(config_dir, exist_ok=True)
        with open(config_path, 'w') as config_file:
            config.write(config_file)

        self.updater = Updater(token=tg_bot_token)
        dispatcher = self.updater.dispatcher

        start_command_handler = CommandHandler('start', self.start_command_callback)
        dispatcher.add_handler(start_command_handler)
        help_command_handler = CommandHandler('help', self.help_command_callback)
        dispatcher.add_handler(help_command_handler)
        clutter_command_handler = CommandHandler('clutter', self.clutter_command_callback)
        dispatcher.add_handler(clutter_command_handler)
        dl_command_handler = CommandHandler('dl', self.dl_command_callback, filters=~ Filters.forwarded, pass_args=True)
        dispatcher.add_handler(dl_command_handler)
        link_command_handler = CommandHandler('link', self.link_command_callback, filters=~ Filters.forwarded,
                                              pass_args=True)
        dispatcher.add_handler(link_command_handler)

        message_with_links_handler = MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) |
                                                                    Filters.entity(MessageEntity.TEXT_LINK)),
                                                    self.message_callback)
        dispatcher.add_handler(message_with_links_handler)

        message_callback_query_handler = CallbackQueryHandler(self.message_callback_query_callback)
        dispatcher.add_handler(message_callback_query_handler)

        inline_query_handler = InlineQueryHandler(self.inline_query_callback)
        dispatcher.add_handler(inline_query_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown_command_callback)
        dispatcher.add_handler(unknown_handler)

        dispatcher.add_error_handler(self.error_callback)

        self.bot_username = self.updater.bot.get_me().username
        self.RANT_TEXT_PRIVATE = "Read /help to learn how to use me"
        self.RANT_TEXT_PUBLIC = "[Press here and start to read help in my PM to learn how to use me](t.me/" + self.bot_username + "?start=1)"

    def start(self, use_webhook=False, app_url=None, webhook_port=None, cert_file=None, webhook_host="0.0.0.0", url_path="scdlbot"):
        if use_webhook:
            url_path = url_path.replace(":", "")
            self.updater.start_webhook(listen=webhook_host,
                                       port=webhook_port,
                                       url_path=url_path)
            self.updater.bot.set_webhook(url=urljoin(app_url, url_path),
                                         certificate=open(cert_file, 'rb') if cert_file else None)
        else:
            self.updater.start_polling()
        # self.send_alert(self.updater.bot, "bot restarted")
        self.updater.idle()

    @staticmethod
    def get_response_text(file_name):
        # https://stackoverflow.com/a/20885799/2490759
        path = '/'.join(('texts', file_name))
        return pkg_resources.resource_string(__name__, path).decode("UTF-8")

    @staticmethod
    def md_italic(text):
        return "".join(["_", text, "_"])

    def log_and_botan_track(self, event_name, message=None):
        logger.info("Event: %s", event_name)
        if message:
            if self.botan_token:
                try:
                    # uid = message.chat_id
                    uid = message.from_user.id
                except AttributeError:
                    logger.warning('No chat_id in message')
                    return False
                data = json.loads(message.to_json())
                return botan.track(self.botan_token, uid, data, event_name)
            else:
                return False

    def send_alert(self, bot, text, url=""):
        for alert_chat_id in self.ALERT_CHAT_IDS:
            try:
                bot.send_message(chat_id=alert_chat_id, text="BOT ADMIN ALERT\nURL or file failed:\n" + url + "\n" + text)
            except:
                pass

    def rant_and_cleanup(self, bot, chat_id, rant_text, reply_to_message_id=None):
        rant_msg = bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                    text=rant_text, parse_mode='Markdown', disable_web_page_preview=True)
        if chat_id in self.NO_CLUTTER_CHAT_IDS:
            if not chat_id in self.rant_msg_ids.keys():
                self.rant_msg_ids[chat_id] = []
            else:
                for rant_msg_id in self.rant_msg_ids[chat_id]:
                    try:
                        bot.delete_message(chat_id=chat_id, message_id=rant_msg_id)
                    except:
                        pass
                    self.rant_msg_ids[chat_id].remove(rant_msg_id)
        self.rant_msg_ids[chat_id].append(rant_msg.message_id)

    def unknown_command_callback(self, bot, update):
        pass
        # bot.send_message(chat_id=update.message.chat_id, text="Unknown command")

    def error_callback(self, bot, update, error):
        try:
            raise error
        except Unauthorized:
            # remove update.message.chat_id from conversation list
            logger.debug('Update {} caused Unauthorized error: {}'.format(update, error))
        except BadRequest:
            # handle malformed requests - read more below!
            logger.debug('Update {} caused BadRequest error: {}'.format(update, error))
        except TimedOut:
            # handle slow connection problems
            logger.debug('Update {} caused TimedOut error: {}'.format(update, error))
        except NetworkError:
            # handle other connection problems
            logger.debug('Update {} caused NetworkError: {}'.format(update, error))
        except ChatMigrated as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
            logger.debug('Update {} caused ChatMigrated error: {}'.format(update, error))
        except TelegramError:
            # handle all other telegram related errors
            logger.debug('Update {} caused TelegramError: {}'.format(update, error))

    def start_command_callback(self, bot, update):
        self.help_command_callback(bot, update, event_name="start")

    def help_command_callback(self, bot, update, event_name="help"):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        reply_to_message_id = update.message.message_id
        self.log_and_botan_track(event_name, update.message)
        if (chat_type != "private") and (chat_id in self.NO_CLUTTER_CHAT_IDS):
            self.rant_and_cleanup(bot, chat_id, self.RANT_TEXT_PUBLIC, reply_to_message_id=reply_to_message_id)
        else:
            bot.send_message(chat_id=chat_id, text=self.HELP_TEXT,
                             parse_mode='Markdown', disable_web_page_preview=True)

    def clutter_command_callback(self, bot, update):
        chat_id = update.message.chat_id
        self.log_and_botan_track("clutter", update.message)
        if chat_id in self.NO_CLUTTER_CHAT_IDS:
            self.NO_CLUTTER_CHAT_IDS.remove(chat_id)
            bot.send_message(chat_id=chat_id,
                             text="Chat cluttering is now ON. I *will send audios as replies* to messages with links.",
                             parse_mode='Markdown', disable_web_page_preview=True)
        else:
            self.NO_CLUTTER_CHAT_IDS.add(chat_id)
            bot.send_message(chat_id=chat_id,
                             text="Chat cluttering is now OFF. I *will not send audios as replies* to messages with links.",
                             parse_mode='Markdown', disable_web_page_preview=True)

    def inline_query_callback(self, bot, update):
        inline_query_id = update.inline_query.id
        text = update.inline_query.query
        results = []
        urls = self.prepare_urls(text=text, get_direct_urls=True)
        if urls:
            self.log_and_botan_track("link_inline")
            for url in urls:
                # self.download_and_send(bot, url, self.STORE_CHAT_ID, inline_query_id=update.inline_query.id)
                for direct_url in urls[url].splitlines():  #TODO: fix non-mp3 and allow only sc/bc
                    logger.debug(direct_url)
                    results.append(InlineQueryResultAudio(id=str(uuid4()), audio_url=direct_url, title="FAST_INLINE_DOWNLOAD"))
        try:
            bot.answer_inline_query(inline_query_id, results)
        except:
            pass

    def dl_command_callback(self, bot, update, args=None, event_name="dl"):
        chat_id = update.message.chat_id
        chat_type = update.message.chat.type
        reply_to_message_id = update.message.message_id
        apologize = not (event_name == "msg" and chat_type != "private")
        if event_name != "msg" and not args:
            rant_text = self.RANT_TEXT_PRIVATE if chat_type == "private" else self.RANT_TEXT_PUBLIC
            rant_text += "\nYou can simply send message with links (to download) OR command as `/{} <links>`.".format(event_name)
            self.rant_and_cleanup(bot, chat_id, rant_text, reply_to_message_id=update.message.message_id)
            return
        if apologize:
            bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        urls = self.prepare_urls(msg=update.message, get_direct_urls=(event_name == "link"))  # text=" ".join(args)
        if not urls:
            if apologize:
                bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                 text=self.NO_URLS_TEXT, parse_mode='Markdown')
            return
        else:
            logger.debug(urls)
            # self.log_and_botan_track("{}_cmd".format(event_name), update.message)
            if event_name == "dl":
                self.log_and_botan_track("dl_cmd", update.message)
                wait_message = bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                                parse_mode='Markdown', text=self.md_italic(self.WAIT_TEXT))
                for url in urls:
                    self.download_url_and_send(bot, url, urls[url], chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                               wait_message_id=wait_message.message_id)
            elif event_name == "link":
                self.log_and_botan_track("link_cmd", update.message)
                link_text = ""
                for i, link in enumerate("\n".join(urls.values()).split()):
                    logger.debug(link)
                    if self.shortener:
                        try:
                            link = self.shortener.short(link)
                        except:
                            pass
                    link_text += "[Download Link #" + str(i + 1) + "](" + link + ")\n"
                bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                 parse_mode='Markdown', text=link_text)
            elif event_name == "msg":
                if chat_type == "private":
                    self.log_and_botan_track("dl_msg", update.message)
                    wait_message = bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                                    parse_mode='Markdown', text=self.md_italic(self.WAIT_TEXT))
                    for url in urls:
                        self.download_url_and_send(bot, url, urls[url], chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                                   wait_message_id=wait_message.message_id)
                else:
                    if "http" in " ".join(urls.values()):
                        self.log_and_botan_track("dl_msg_income")
                        orig_msg_id = str(reply_to_message_id)
                        if not chat_id in self.msg_store.keys():
                            self.msg_store[chat_id] = {}
                        self.msg_store[chat_id][orig_msg_id] = {"message": update.message, "urls": urls}
                        button_dl = InlineKeyboardButton(text="✅ Yes", callback_data=" ".join([orig_msg_id, "dl"]))
                        button_link = InlineKeyboardButton(text="✅ Get links", callback_data=" ".join([orig_msg_id, "link"]))
                        button_cancel = InlineKeyboardButton(text="❎ No", callback_data=" ".join([orig_msg_id, "nodl"]))
                        inline_keyboard = InlineKeyboardMarkup([[button_dl, button_cancel]])
                        question = "🎶 links found. Download it?"
                        bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                         reply_markup=inline_keyboard, text=question)


    def link_command_callback(self, bot, update, args=None):
        self.dl_command_callback(bot, update, args, event_name="link")

    def message_callback(self, bot, update):
        self.dl_command_callback(bot, update, event_name="msg")

    def message_callback_query_callback(self, bot, update):
        chat_id = update.callback_query.message.chat_id
        btn_msg_id = update.callback_query.message.message_id
        orig_msg_id, action = update.callback_query.data.split()
        if chat_id in self.msg_store:
            if orig_msg_id in self.msg_store[chat_id]:
                self.log_and_botan_track("_".join([action, "msg"]), self.msg_store[chat_id][orig_msg_id]["message"])
                if action == "dl":
                    update.callback_query.answer(text=self.WAIT_TEXT)
                    edited_msg = update.callback_query.edit_message_text(parse_mode='Markdown',
                                                                         text=self.md_italic(self.WAIT_TEXT))
                    urls = self.msg_store[chat_id][orig_msg_id]["urls"]
                    for url in urls:
                        self.download_url_and_send(bot, url, urls[url], chat_id=chat_id, reply_to_message_id=orig_msg_id,
                                                   wait_message_id=edited_msg.message_id)
                elif action == "nodl":
                    # update.callback_query.answer(text="Cancelled!", show_alert=True)
                    bot.delete_message(chat_id=chat_id, message_id=btn_msg_id)
                elif action == "link":
                    pass
                self.msg_store[chat_id].pop(orig_msg_id)
                for msg_id in self.msg_store[chat_id]:
                    timedelta = datetime.now() - self.msg_store[chat_id][msg_id]["message"].date
                    if timedelta.days > 0:
                        self.msg_store[chat_id].pop(msg_id)
                return
        update.callback_query.answer(text="Sorry, very old message that I don't remember.")
        bot.delete_message(chat_id=chat_id, message_id=btn_msg_id)

    @staticmethod
    def youtube_dl_download_url(url, ydl_opts, queue=None):
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        try:
            ydl.download([url])
        except Exception as exc:
            ydl_status = str(exc)
            # ydl_status = exc  #TODO
        else:
            ydl_status = 0
        if queue:
            queue.put(ydl_status)

    def youtube_dl_get_direct_urls(self, url):
        ret_code, std_out, std_err = self.youtube_dl["--get-url", url].run(retcode=None)
        # TODO: case when one page has multiple videos some available some not
        if "returning it as such" in std_err:
            return "direct"
        elif "proxy server" in std_err:
            return "proxy"
        elif "yt_live_broadcast" in std_out:
            return "live"
        else:
            return std_out

    def prepare_urls(self, msg=None, text=None, get_direct_urls=False):
        if text:
            urls = find_all_links(text, default_scheme="http")
        elif msg:
            urls = []
            for url_str in msg.parse_entities(types=["url"]).values():
                if "://" not in url_str:
                    url_str = "http://" + url_str
                urls.append(URL(url_str))
        else:
            logger.debug("Text or msg is required")
            return
        urls_dict = {}
        for url in urls:
            url_text = url.to_text(True)
            url_parts_num = len([part for part in url.path_parts if part])
            if (
                # SoundCloud: tracks, sets and widget pages
                (self.SITES["sc"] in url.host and (2 <= url_parts_num <= 3 or self.SITES["scapi"] in url_text)) or
                # Bandcamp: tracks and albums
                (self.SITES["bc"] in url.host and (2 <= url_parts_num <= 2)) or
                # YouTube: videos and playlists
                (self.SITES["yt"] in url.host and (
                    "youtu.be" in url.host or "watch" in url.path or "playlist" in url.path))
            ):
                if get_direct_urls or self.SITES["yt"] in url.host:
                    direct_urls = self.youtube_dl_get_direct_urls(url_text)
                    if direct_urls:
                        urls_dict[url_text] = direct_urls
                else:
                    urls_dict[url_text] = "http"
            elif not any((site in url.host for site in self.SITES.values())):
                direct_urls = self.youtube_dl_get_direct_urls(url_text)
                if direct_urls:
                    urls_dict[url_text] = direct_urls
        if not urls_dict:
            logger.info("No supported URLs found")
        return urls_dict

    @run_async
    def download_url_and_send(self, bot, url, direct_urls, chat_id, reply_to_message_id=None,
                              wait_message_id=None, inline_query_id=None):
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_AUDIO)
        download_dir = os.path.join(self.DL_DIR, str(uuid4()))
        shutil.rmtree(download_dir, ignore_errors=True)
        os.makedirs(download_dir)

        scdl_cmd = self.scdl[
            "-l", url,  # URL of track/playlist/user
            "-c",  # Continue if a music already exist
            "--path", download_dir,  # Download the music to a custom path
            "--onlymp3",  # Download only the mp3 file even if the track is Downloadable
            "--addtofile",  # Add the artist name to the filename if it isn't in the filename already
        ]
        bandcamp_dl_cmd = self.bandcamp_dl[
            "--base-dir", download_dir,  # Base location of which all files are downloaded
            "--template", "%{track} - %{artist} - %{title} [%{album}]",  # Output filename template
            "--overwrite",  # Overwrite tracks that already exist
            "--group",  # Use album/track Label as iTunes grouping
            "--embed-art",  # Embed album art (if available)
            "--no-slugify",  # Disable slugification of track, album, and artist names
            url  # URL of album/track
        ]
        # TODO: different ydl_opts for different sites
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # %(autonumber)s - %(title)s-%(id)s.%(ext)s
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                },
                # {
                #     'key': 'EmbedThumbnail',
                # },
                # {
                #     'key': 'FFmpegMetadata',
                # },
            ],
        }

        status = 0
        if direct_urls == "direct":
            status = -3
        elif direct_urls == "proxy":
            status = -4
        elif direct_urls == "live":
            status = -5
        else:
            logger.info("Trying to download URL: %s", url)
            if self.SITES["sc"] in url and self.SITES["scapi"] not in url:
                logger.info("scdl starts...")
                try:
                    cmd_popen = scdl_cmd.popen(stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                    try:
                        std_out, std_err = cmd_popen.communicate(timeout=self.DL_TIMEOUT)
                        if cmd_popen.returncode or "Error resolving url" in std_err:
                            text = "scdl process failed" + "\nstdout:\n" + std_out + "\nstderr:\n" + std_err
                            logger.error(text)
                            self.send_alert(bot, text, url)
                        else:
                            text = "scdl succeeded"
                            logger.info(text)
                            status = 1
                    except TimeoutExpired:
                        text = "Download took with scdl too long, dropped"
                        logger.warning(text)
                        cmd_popen.kill()
                        status = -1
                except Exception as exc:
                    text = "scdl start failed"
                    logger.exception(text)
                    self.send_alert(bot, text + "\n" + str(exc), url)
            elif self.SITES["bc"] in url:
                logger.info("bandcamp-dl starts...")
                try:
                    cmd_popen = bandcamp_dl_cmd.popen(stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                    try:
                        std_out, std_err = cmd_popen.communicate(input="yes", timeout=self.DL_TIMEOUT)
                        if cmd_popen.returncode:
                            text = "bandcamp-dl process failed" + "\nstdout:\n" + std_out + "\nstderr:\n" + std_err
                            logger.error(text)
                            self.send_alert(bot, text, url)
                        else:
                            text = "bandcamp-dl succeeded"
                            logger.info(text)
                            status = 1
                    except TimeoutExpired:
                        text = "bandcamp-dl took too much time and dropped"
                        logger.warning(text)
                        cmd_popen.kill()
                        status = -1
                except Exception as exc:
                    text = "bandcamp-dl start failed"
                    logger.exception(text)
                    self.send_alert(bot, text + "\n" + str(exc), url)

        if status == 0:
            logger.info("youtube-dl starts...")
            queue = multiprocessing.Queue()
            ydl = multiprocessing.Process(target=self.youtube_dl_download_url, args=(url, ydl_opts, queue,))
            ydl.start()
            try:
                ydl_status = queue.get(block=True, timeout=self.DL_TIMEOUT)
                ydl.join()
                if ydl_status:
                    raise Exception(ydl_status)
                    # raise ydl_status
                text = "youtube-dl succeeded"
                logger.info(text)
                status = 1
            except Empty:
                ydl.join(1)
                if ydl.is_alive():
                    ydl.terminate()
                text = "youtube-dl took too much time and dropped"
                logger.warning(text)
                status = -1
            except Exception as exc:
                text = "youtube-dl failed"
                logger.exception(text)
                self.send_alert(bot, text + "\n" + str(exc), url)
                status = -2
            gc.collect()

        if status == -1:
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.DL_TIMEOUT_TEXT, parse_mode='Markdown')
        elif status == -2:
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.NO_AUDIO_TEXT, parse_mode='Markdown')
        elif status == -3:
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.DIRECT_RESTRICTION_TEXT, parse_mode='Markdown')
        elif status == -4:
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.REGION_RESTRICTION_TEXT, parse_mode='Markdown')
        elif status == -5:
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.LIVE_RESTRICTION_TEXT, parse_mode='Markdown')
        elif status == 1:
            if chat_id in self.NO_CLUTTER_CHAT_IDS:
                reply_to_message_id = None
            file_list = []
            for d, dirs, files in os.walk(download_dir):
                for file in files:
                    file_list.append(os.path.join(d, file))
            for file in sorted(file_list):
                self.split_and_send_audio_file(bot, chat_id, reply_to_message_id, file)

        shutil.rmtree(download_dir, ignore_errors=True)

        if wait_message_id:  # TODO: delete only once
            try:
                bot.delete_message(chat_id=chat_id, message_id=wait_message_id)
            except:
                pass

        # if inline_query_id:
        #     results = []
        #     for audio_id in sent_audio_ids:
        #         if audio_id:
        #             results.append(InlineQueryResultCachedAudio(id=str(uuid4()), audio_file_id=audio_id))
        #     bot.answer_inline_query(inline_query_id, results)

        # downloader = URLopener()

        #     try:
        #         file_name, headers = downloader.retrieve(url.to_text(full_quote=True))
        #         patoolib.extract_archive(file_name, outdir=DL_DIR)
        #         os.remove(file_name)
        #     except Exception as exc:
        #         return str(exc)
        #     #     return str(sys.exc_info()[0:1])
        #
        # return "success"

    def split_and_send_audio_file(self, bot, chat_id, reply_to_message_id=None, file=""):
        sent_audio_ids = []
        file_root, file_ext = os.path.splitext(file)
        file_format = file_ext.replace(".", "")
        if not (file_format == "mp3" or file_format == "m4a" or file_format == "mp4"):
            logger.warning("Unsupported file format: %s", file)
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text="Sorry, downloaded file is in format I could not yet send or convert.")
            return
        file_size = os.path.getsize(file)
        if file_size > self.MAX_CONVERT_FILE_SIZE:
            logger.warning("Large file for convert: %s", file)
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text="Sorry, downloaded file is larger than I could convert.")
            return
        parts_number = 1
        file_parts = []
        if file_size <= self.MAX_TG_FILE_SIZE:
            file_parts.append(file)
        else:
            logger.info("Splitting: %s", file)
            try:
                id3 = mutagen.id3.ID3(file, translate=False)
            except:
                id3 = None
            parts_number = file_size // self.MAX_TG_FILE_SIZE + 1
            try:
                sound = AudioSegment.from_file(file, file_format)
                part_size = len(sound) / parts_number
                for i in range(parts_number):
                    file_part = file.replace(file_ext, ".part" + str(i + 1) + file_ext)
                    part = sound[part_size * i:part_size * (i + 1)]
                    part.export(file_part, format="mp3")
                    del part
                    if id3:
                        id3.save(file_part, v1=2, v2_version=4)
                    file_parts.append(file_part)
                # https://github.com/jiaaro/pydub/issues/135
                # https://github.com/jiaaro/pydub/issues/89#issuecomment-75245610
                del sound
                gc.collect()
            except (OSError, MemoryError) as exc:
                text = "Failed pydub convert"
                logger.exception(text)
                self.send_alert(bot, text + "\n" + str(exc), file)
                bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                 text="Not enough memory to convert, you may try again later..")
                gc.collect()
                return
        total_status = 0
        for index, file in enumerate(file_parts):
            logger.info("Sending: %s", file)
            bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_AUDIO)
            # file = translit(file, 'ru', reversed=True)
            if chat_id in self.NO_CLUTTER_CHAT_IDS:
                caption = ""
            else:
                caption = "Downloaded with @{}".format(self.bot_username)
            if file_size > self.MAX_TG_FILE_SIZE:
                caption += "\n" + " ".join(["Part", str(index + 1), "of", str(parts_number)])
            status = 0
            for i in range(3):
                try:
                    audio_msg = bot.send_audio(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                                               audio=open(file, 'rb'), caption=caption)
                    sent_audio_ids.append(audio_msg.audio.file_id)
                    status = 1
                    total_status = 1
                    break
                except TelegramError as exc:
                    logger.exception("Sending failed because of TelegramError: %s", file)
                    self.send_alert(bot, "TelegramError:\n" + str(exc), file)
            if status:
                logger.info("Sending success: %s", file)
            else:
                logger.warning("Sending failed: %s", file)
        if not total_status:
            logger.warning("Sending total failed: %s", file)
            bot.send_message(chat_id=chat_id, reply_to_message_id=reply_to_message_id,
                             text=self.NO_AUDIO_TEXT, parse_mode='Markdown')
