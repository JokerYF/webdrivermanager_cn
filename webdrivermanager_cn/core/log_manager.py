import logging

__logger = logging.getLogger('WDM')
__logger_level = logging.DEBUG


def wdm_logger():
    return __logger


def set_logger(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise Exception(f'logger 类型不正确！{logger}')

    global __logger
    __logger = logger


def set_logger_init():
    if __logger.name != 'WDM':
        return

    # log 等级
    __logger.setLevel(__logger_level)

    # log 格式
    log_format = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt=log_format)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    __logger.addHandler(stream)


# if init_log():
set_logger_init()
