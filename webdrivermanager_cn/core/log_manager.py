import logging

LOGGER = logging.getLogger('WDM')
LOGGER_INIT_FLAG = False


def set_logger(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise Exception(f'logger 类型不正确！{logger}')

    global LOGGER
    LOGGER = logger


class LogMixin:
    """
    log 混入类
    """

    @property
    def log(self):
        global LOGGER
        return LOGGER

    @staticmethod
    def set_logger_init():
        from webdrivermanager_cn.core.config import init_log, init_log_level

        global LOGGER_INIT_FLAG
        global LOGGER

        # 如果当前logger不是wdm，或者不需要输出log的话，直接返回
        if LOGGER.name != 'WDM' or not init_log():
            return

        # 如果已经初始化过默认logger的属性，直接返回
        if LOGGER_INIT_FLAG:
            return

        LOGGER_INIT_FLAG = True

        # log 等级
        LOGGER.setLevel(init_log_level())

        # log 格式
        log_format = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"
        formatter = logging.Formatter(fmt=log_format)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        LOGGER.addHandler(stream)
