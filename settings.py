from dotenv import load_dotenv
from logging.config import dictConfig


load_dotenv()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "brief": {
            "format": "%(message)s",
        },
        "usually": {
            "format": "[%(name)s]: %(message)s",
        },
        "default": {
            "format": "%(asctime)s (%(levelname)s) [%(name)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
     "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "usually": {
            "formatter": "usually",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "propagate": False,
            "level": "INFO",
        },
        "__main__": {
            "handlers": ["default"],
            "propagate": False,
            "level": "DEBUG",
        },
        "test": {
            "handlers": ["default"],
            "propagate": False,
            "level": "DEBUG",
        },
        "telegram.ext.updater": {
            "handlers": ["usually"],
            "propagate": False,
            "level": "INFO",
        },
        "telegram.vendor.ptb_urllib3.urllib3.connectionpool": {
            "handlers": ["default"],
            "propagate": False,
            "level": "ERROR",
        }
    }
}
dictConfig(LOGGING_CONFIG)