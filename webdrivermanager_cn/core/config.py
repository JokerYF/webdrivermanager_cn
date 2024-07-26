# ------------------
# Driver 源相关
# ------------------
import logging

from urllib3 import disable_warnings

from webdrivermanager_cn.core.mixin import EnvMixin


# ------------------
# WDM 全局变量
# ------------------

def str2bool(value):
    if isinstance(value, bool):
        return value
    return value.lower() in ['true', '1']


__env = EnvMixin()


def init_log():
    """
    是否初始化WDM默认logger
    默认为 False
    执行以下代码为开启
    os.environ['WDM_LOG'] = 'true'
    :return:
    """
    try:
        return str2bool(__env.get('WDM_LOG', False))
    except:
        return False


def init_log_level():
    """
    初始化默认WDM日志等级
    当 init_log 函数返回值为 True 时生效
    执行以下代码修改
    os.environ['WDM_LOG_LEVEL'] = f'{logging.INFO}'
    :return:
    """
    default = logging.INFO
    try:
        return int(__env.get('WDM_LOG_LEVEL', default))
    except:
        return default


def clear_wdm_cache_time():
    """
    清理超过时间的 WebDriver
    默认为 5 天
    执行以下代码修改
    os.environ['WDM_CACHE_TIME'] = 5
    :return:
    """
    default = 5
    try:
        return int(__env.get('WDM_CACHE_TIME', default))
    except:
        return default


def verify_not():
    """
    禁用SSL认证（代理）
    默认为 False
    执行以下代码修改
    os.environ['WDM_VERIFY'] = 'true'
    :return:
    """
    default = False
    try:
        return str2bool(__env.get('WDM_VERIFY', default))
    except:
        return default


if not verify_not():
    disable_warnings()


def request_timeout():
    """
    请求超时时间
    默认为 10 秒
    执行以下代码修改
    os.environ['WDM_TIMEOUT'] = '10'
    :return:
    """
    default = 10
    try:
        return int(__env.get('WDM_TIMEOUT', default))
    except:
        return default
