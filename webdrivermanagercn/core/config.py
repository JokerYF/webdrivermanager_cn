import logging
import os.path
import sys

ChromeDriverUrl = 'https://registry.npmmirror.com/-/binary/chromedriver/'
ChromeDriverUrlNew = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/'

# log相关
write_log = True
default_formatter = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"

wdm_log_write = True
wdm_log_write_path = os.path.join(sys.path[0], 'wdm.log')
wdm_log_write_level = logging.DEBUG
wdm_log_write_formatter = default_formatter

wdm_log_console = True
wdm_log_console_level = logging.DEBUG
wdm_log_console_formatter = default_formatter

__wdm_logger = logging.Logger(wdm_log_write_path)

if wdm_log_console:
    stream = logging.StreamHandler()
    stream.setLevel(wdm_log_console_level)
    stream.setFormatter(logging.Formatter(wdm_log_console_formatter))
    __wdm_logger.addHandler(stream)

if wdm_log_write:
    writer = logging.FileHandler(wdm_log_write_path, encoding='utf-8')
    writer.setLevel(wdm_log_write_level)
    writer.setFormatter(logging.Formatter(wdm_log_write_formatter))
    __wdm_logger.addHandler(writer)

wdm_logger = __wdm_logger if write_log else logging.getLogger("WDM")


def set_logger(logger: logging.Logger = None):
    global wdm_logger
    if logger:
        wdm_logger = logger
