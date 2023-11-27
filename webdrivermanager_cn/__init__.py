from chrome import ChromeDriverManager
from geckodriver import GeckodriverManager
from microsoft import EdgeWebDriverManager

VERSION = '1.2.0'

__all__ = [
    'VERSION',
    'ChromeDriverManager',
    'EdgeWebDriverManager',
    'GeckodriverManager',
]
