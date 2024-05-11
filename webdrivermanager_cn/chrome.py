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
            latest: 自动获取当前安装的Chrome版本最新的ChromeDriver版本号，如果获取失败则拉取最新的发行版本号
            xxx.xxx.xxx.xxx: 指定的具体ChromeDriver版本号
        :param path:
        """
        self.chromedriver = ChromeDriver(version=version, path=path)

    def install(self):
        """
        下载chromedriver，并返回本地路径
        :return:
        """
        return self.chromedriver.install()
