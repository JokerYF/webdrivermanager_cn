import logging

from webdrivermanager_cn.core.config import init_log, init_log_level

__logger = logging.getLogger('WDM')
__logger_init_flag = False


def wdm_logger():
    return __logger


def set_logger(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise Exception(f'logger 类型不正确！{logger}')

    global __logger
    __logger = logger


def set_logger_init():
    global __logger_init_flag

    if (__logger_init_flag
            or __logger.name != 'WDM'
            or not init_log()):
        return

    __logger_init_flag = True

    # log 等级
    __logger.setLevel(init_log_level())

    # log 格式
    log_format = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt=log_format)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    __logger.addHandler(stream)
