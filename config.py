msg_logs_file = "all_messages.logs"

LOGGING_CONFIG = {
    "version": 1,
    'filters': {
        'wrapperHelper': {
            '()': "settings.wrapperHelper",
        },
        "messageFilter": {
            "()": "settings.messageFilter",
        },
    },
    "disable_existing_loggers": False,
    "formatters": {
        "brief": {
            "format": "%(message)s",
        },
        "usually": {
            "format": "[%(name)s]: %(message)s",
        },
        "light": {
            "format": "{asctime} {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "default": {
            "format": "{asctime} ({levelname:^7}) - [{name}.{funcName}()] - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
     "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            'filters': ['wrapperHelper'],
        },
        "usually": {
            "formatter": "usually",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "msg_to_file": {
            "formatter": "light",
            "class": "logging.FileHandler",
            "filename": msg_logs_file,
            "encoding": "utf8",
            "filters": ["messageFilter"],
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "propagate": False,
            "level": "INFO",
        },
        "__main__": {
            "handlers": ["default", "msg_to_file"],
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