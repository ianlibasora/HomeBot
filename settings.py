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
            "filename": "logs/infos.log",
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
