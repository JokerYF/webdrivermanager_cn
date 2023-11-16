# ------------------
# Driver 源相关
# ------------------
import logging
import os

# ChromeDriver 源地址
ChromeDriverUrl = 'https://registry.npmmirror.com/-/binary/chromedriver'
ChromeDriverUrlNew = 'https://registry.npmmirror.com/-/binary/chrome-for-testing'
ChromeDriver = 'https://googlechromelabs.github.io/chrome-for-testing'

# Firefox 驱动源地址
GeckodriverUrl = 'https://registry.npmmirror.com/-/binary/geckodriver'
GeckodriverApi = 'https://api.github.com/repos/mozilla/geckodriver/releases'

# Edge 驱动源地址
EdgeDriverUrl = 'https://msedgedriver.azureedge.net'


# ------------------
# WDM 全局变量
# ------------------

def str2bool(value):
    if isinstance(value, bool):
        return value
    return value.lower() in ['true', '1']


def init_log():
    """
    是否初始化WDM默认logger
    默认为False
    执行以下代码为开启
    os.environ['WDM_LOG'] = 'true'
    :return:
    """
    try:
        return str2bool(os.getenv('WDM_LOG', False))
    except:
        return False


def init_log_level():
    """
    初始化默认WDM日志等级
    当 init_log 函数返回值为True时生效
    执行以下代码修改
    os.environ['WDM_LOG_LEVEL'] = f'{logging.INFO}'
    :return:
    """
    default = logging.INFO
    try:
        return int(os.getenv('WDM_LOG_LEVEL', default))
    except:
        return default


def clear_wdm_cache_time():
    """
    清理超过时间的 WebDriver
    默认为5天
    执行以下代码修改
    os.environ['WDM_CACHE_TIME'] = 5
    :return:
    """
    default = 5
    try:
        return int(os.getenv('WDM_CACHE_TIME', default))
    except:
        return default
