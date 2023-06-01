import threading
import telebot
from user import UserFSM
from admin import AdminFSM
from Db.database import Database1
from Db.config import Config
from options import settings
import logging
from options import log_settings
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, current_fsm_dict_admin, current_fsm_dict_user):
        self.bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=True)
        self.db_host = settings.DATABASE_HOST
        self.db_name = settings.DATABASE
        self.db_user = settings.DATABASE_USER
        self.db_port = settings.DATABASE_PORT
        self.db_password = settings.DATABASE_PASSWD
        self.db = Database1(self.db_host, self.db_port, self.db_user, self.db_password, self.db_name)
        self.config = Config(self.db)
        self.current_fsm_dict_lock = threading.RLock()
        self.current_fsm_dict_admin = current_fsm_dict_admin
        self.current_fsm_dict_user = current_fsm_dict_user
        self.message_handler = MessageHandler(self.bot)
        self.user = User(self.bot, self.config, self.current_fsm_dict_lock, self.current_fsm_dict_admin,
                         self.message_handler)
        self.admin = Admin(self.bot, self.config, self.current_fsm_dict_lock, self.current_fsm_dict_user,
                           self.message_handler)
        self.message_handler.get_user(self.user)
        self.message_handler.get_admin(self.admin)

    def polling(self):
        self.bot.infinity_polling()


class Admin:
    def __init__(self, bot, config, current_fsm_dict_lock, user, message_handler):
        self.bot = bot
        self.current_fsm_dict_admin = dict()
        self.config = config
        self.current_fsm_dict_lock = current_fsm_dict_lock
        self.current_fsm_dict_user = user
        self.user = None
        self.message_handler = message_handler

        @self.bot.message_handler(commands=['admin'])
        def launch_admin(call):
            self.start_fsm_admin(call)

    def start_fsm_admin(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_user.get(telegram_id) is not None:
                self.current_fsm_dict_user[telegram_id].is_finished_user()
                self.current_fsm_dict_user.pop(telegram_id)
            self.current_fsm_dict_admin[telegram_id] = AdminFSM(self.bot, self.config,
                                                                self.process_message_admin)
            self.message_handler.get_user_fsm_dict(self.current_fsm_dict_admin)
            self.message_handler.get_admin_process_message(self.process_message_admin)
            self.current_fsm_dict_admin[telegram_id].start_admin(call)

    def run_fsm_admin(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_admin.get(telegram_id) is not None:
                self.current_fsm_dict_admin[telegram_id].run_admin(call)
                if self.current_fsm_dict_admin[telegram_id].is_finished_admin():
                    self.current_fsm_dict_admin[telegram_id] = None

    def process_message_admin(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_admin.get(telegram_id) is not None:
                self.run_fsm_admin(call)


class User:
    def __init__(self, bot, config, current_fsm_dict_lock, admin, message_handler):
        self.bot = bot
        self.config = config
        self.current_fsm_dict_lock = current_fsm_dict_lock
        self.current_fsm_dict_user = dict()
        self.current_fsm_dict_admin = admin
        self.admin = None
        self.message_handler = message_handler

        @self.bot.message_handler(commands=['start'])
        def launch_user(call):
            self.start_fsm_user(call)

    def start_fsm_user(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_admin.get(telegram_id) is not None:
                self.current_fsm_dict_admin[telegram_id].is_finished_admin()
                self.current_fsm_dict_admin[telegram_id] = None
                self.current_fsm_dict_admin.pop(telegram_id)
            self.current_fsm_dict_user[telegram_id] = UserFSM(self.bot, self.process_message_user,
                                                              self.config)
            self.message_handler.get_user_fsm_dict(self.current_fsm_dict_user)
            self.message_handler.get_user_process_message(self.process_message_user)
            self.current_fsm_dict_user[telegram_id].start(call)

    def run_fsm_user(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_user.get(telegram_id) is not None:
                self.current_fsm_dict_user[telegram_id].run_user(call)
                if self.current_fsm_dict_user[telegram_id].is_finished_user():
                    self.current_fsm_dict_user[telegram_id] = None

    def process_message_user(self, call):
        telegram_id = call.from_user.id
        with self.current_fsm_dict_lock:
            if self.current_fsm_dict_user.get(telegram_id) is not None:
                self.run_fsm_user(call)


class MessageHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_fsm_dict = dict()
        self.admin_fsm_dict = dict()
        self.process_message_user = None
        self.process_message_admin = None
        self.admin = None
        self.user = None

        @self.bot.message_handler(content_types=['text'])
        @self.bot.callback_query_handler(func=lambda call: True)
        def call_process_message(call):
            telegram_id = call.from_user.id
            if not hasattr(call, "data"):
                if call.text == '/admin':
                    self.admin.start_fsm_admin(call)
                    return
                if call.text == '/start':
                    self.user.start_fsm_user(call)
            if self.user_fsm_dict.get(telegram_id) is not None:
                self.process_message_user(call)
            elif self.admin_fsm_dict.get(telegram_id) is not None:
                self.process_message_admin(call)

    def get_user_process_message(self, user_process_message):
        self.process_message_user = user_process_message

    def get_admin_process_message(self, admin_process_message):
        self.process_message_user = admin_process_message

    def get_user_fsm_dict(self, user_fsm_dict):
        self.user_fsm_dict = user_fsm_dict

    def get_admin_fsm_dict(self, admin_fsm_dict):
        self.admin_fsm_dict = admin_fsm_dict

    def get_admin(self, admin):
        self.admin = admin

    def get_user(self, user):
        self.user = user


def setup_logging(level):
    log_settings.setup_logging(level, settings.DEBUG_FILE_PATH, settings.INFO_FILE_PATH)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)


if __name__ == '__main__':
    admin_dict = dict()
    user_dict = dict()
    bt = TelegramBot(admin_dict, user_dict)
    setup_logging(settings.LOGGING_LEVEL)
    bt.polling()
