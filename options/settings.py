import logging
import dotenv
import os

environ = os.environ
DATA_DIR = environ.get("DATA_DIR", "data")
DEFAULT_DOTENV_PATH = os.path.join(DATA_DIR, '.env')
dotenv_path = environ.get('DOTENV_PATH', DEFAULT_DOTENV_PATH)
dotenv.load_dotenv(dotenv_path)

DEBUG_FILE_PATH = environ.get('DEBUG_FILE_PATH', os.path.join(DATA_DIR, 'debug.log'))
INFO_FILE_PATH = environ.get('INFO_FILE_PATH', os.path.join(DATA_DIR, 'info.log'))

BOT_TOKEN = environ["BOT_TOKEN"]
ADMIN_PASSWORD = environ["ADMIN_PASSWORD"]
LANGUAGE = environ["LANGUAGE"]
LANGUAGE_BUTTONS = environ["LANGUAGE_BUTTONS"]

DATABASE_HOST = environ["DATABASE_HOST"]
DATABASE_USER = environ["DATABASE_USER"]
DATABASE_PASSWD = environ["DATABASE_PASSWD"]
DATABASE_PORT = int(environ["DATABASE_PORT"])
DATABASE = environ["DATABASE"]


LOGGING_LEVEL = logging.DEBUG if environ["LOGGING_LEVEL"] == 'DEBUG' \
    else logging.INFO if environ["LOGGING_LEVEL"] == 'INFO' \
    else None
