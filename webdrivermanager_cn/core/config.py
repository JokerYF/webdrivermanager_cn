# ------------------
# Driver 源相关
# ------------------
# ChromeDriver 源地址
import os

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
        print(123123, os.getenv('WDM_LOG'))
        return str2bool(os.getenv('WDM_LOG', False))
    except Exception as e:
        print(123, e)
        return False


def init_log_level():
    """
    初始化默认WDM日志等级
    当 init_log 函数返回值为True时生效
    执行以下代码修改
    os.environ['WDM_LOG_LEVEL'] = '20'
    :return:
    """
    default = 20
    try:
        return int(os.getenv('WDM_LOG_LEVEL', default))
    except:
        return default
