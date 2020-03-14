from dotenv import load_dotenv
from logging.config import dictConfig
import logging
from config import LOGGING_CONFIG

def fix_main_name(record):
    if record.name == "__main__":
        record.name = "main"

def fix_wrapper(record):
    if record.funcName == "wrapper":
        record.funcName = record.func_name
        record.is_wrapper = True

def is_wrapper(record):
    fix_wrapper(record)
    return hasattr(record, "is_wrapper")

class wrapperHelper(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        fix_main_name(record)
        fix_wrapper(record)
        return True

class messageFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        fix_main_name(record)
        return is_wrapper(record)

load_dotenv()
dictConfig(LOGGING_CONFIG)