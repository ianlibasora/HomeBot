#!/usr/bin/env python3

import logging
from logging.config import dictConfig
from os import getenv
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR_PATH = Path(__file__).parent
COGS_DIR = "cmds"
COGS_DIR_PATH = BASE_DIR_PATH.joinpath(COGS_DIR)
BOT_TOKEN = getenv("TOKEN")
BOT_CHANNEL_ID = int(getenv("BOT_CHANNEL_ID"))
HTTP_TIMEOUT = 10

# LOGS
LOGS_DIR = "logs"
LOGS_DIR_PATH = BASE_DIR_PATH.joinpath(LOGS_DIR)
LOG_FILE = "info.log"
LOG_FILE_PATH = LOGS_DIR_PATH.joinpath(LOG_FILE)
LOGS_DIR_PATH.mkdir(exist_ok=True)

# F1
F1_SCHEDULE_REMINDER_DAY = 0 # Monday
F1_SCHEDULE_REMINDER_HOUR = 9
F1_SCHEDULE_REMINDER_MINUTE = 0


LOGGING_CONFIG = {
    "version": 1,
    "disabled_existring_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)-10s - %(ascitime)s - %(module)-15s : %(message)s"},
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(LOG_FILE_PATH),
            "mode": "w",
            "formatter": "standard"
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        },
    }
}

dictConfig(LOGGING_CONFIG)
