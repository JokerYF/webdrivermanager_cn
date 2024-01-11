"""
ChromeDriver
"""
from webdrivermanager_cn.drivers.chrome import ChromeDriver


class ChromeDriverManager:
    """
    ChromeDriver管理器
    """

    def __init__(self, version='latest', path=None):
        """
        ChromeDriver管理器
        :param version:
        :param path:
        """
        self.chromedriver = ChromeDriver(version=version, path=path)

    def install(self):
        """
        下载chromedriver，并返回本地路径
        :return:
        """
        return self.chromedriver.install()
