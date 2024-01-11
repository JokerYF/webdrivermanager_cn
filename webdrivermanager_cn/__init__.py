from webdrivermanager_cn.chrome import ChromeDriverManager
from webdrivermanager_cn.geckodriver import GeckodriverManager
from webdrivermanager_cn.microsoft import EdgeWebDriverManager

VERSION = '1.2.4'

__all__ = [
    'VERSION',
    'ChromeDriverManager',
    'EdgeWebDriverManager',
    'GeckodriverManager',
]
