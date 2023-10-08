import logging

from webdrivermanager_cn.core.config import init_log, init_log_level

__logger = logging.getLogger('WDM')


def wdm_logger():
    return __logger


def set_logger(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise Exception(f'logger 类型不正确！{logger}')

    global __logger
    __logger = logger


def set_logger_init():
    if __logger.name != 'WDM' or not init_log():
        return

    # log 等级
    __logger.setLevel(init_log_level())

    # log 格式
    log_format = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt=log_format)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    __logger.addHandler(stream)


