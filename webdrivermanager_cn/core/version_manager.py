"""
搜索版本，如果版本不存在，则找比当前小一版本
"""
import os
import re
import subprocess

from packaging import version as vs

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.os_manager import OSManager, OSType
from webdrivermanager_cn.core.request import request_get


class ClientType:
    Chrome = "google-chrome"
    Chromium = "chromium"
    Edge = "edge"
    Firefox = "firefox"
    Safari = "safari"


CLIENT_PATTERN = {
    ClientType.Chrome: r"\d+\.\d+\.\d+\.\d+",
    ClientType.Firefox: r"\d+\.\d+\.\d+",
    ClientType.Edge: r"\d+\.\d+\.\d+\.\d+",
}


class GetUrl(LogMixin):
    """
    根据版本获取url
    """

    def __init__(self):
        self._version = ""

    @property
    def version_obj(self):
        """
        获取版本解析对象
        :return:
        """
        return vs.parse(self._version)

    @property
    def is_new_version(self):
        """
        判断是否为新版本（chrome）
        :return:
        """
        return self.version_obj.major >= 115

    @property
    def get_host(self):
        """
        根据判断获取chromedriver的url
        :return:
        """
        return config.ChromeDriverUrlNew if self.is_new_version else config.ChromeDriverUrl

    @property
    def _version_list(self):
        """
        解析driver url，获取所有driver版本
        :return:
        """
        response_data = request_get(self.get_host).json()
        return [i["name"].replace("/", "") for i in response_data if 'LATEST' not in i]

    def _get_chrome_correct_version(self):
        """
        根据Chrome版本，返回源上找到合适的ChromeDriver版本
        :return:
        """
        _chrome_version = f'{self.version_obj.major}.{self.version_obj.minor}.{self.version_obj.micro}'

        # 根据json获取符合版本的版本号
        data = request_get(config.ChromeDriverLastPatchVersion).json()
        try:
            return data['builds'][_chrome_version]['version']
        except KeyError:
            self.log.warning(
                f'当前chrome版本: {_chrome_version}, '
                f'没有找到合适的ChromeDriver版本 - {config.ChromeDriverLastPatchVersion}'
            )
            # 拉取符合版本list并获取最后一个版本号
            _chrome_version_list = [i for i in self._version_list if _chrome_version in i and 'LATEST' not in i]
            _chrome_version_list = sorted(_chrome_version_list, key=lambda x: tuple(map(int, x.split('.'))))
            return _chrome_version_list[-1]


class GetClientVersion(GetUrl, LogMixin):
    """
    获取当前环境下浏览器版本
    """

    def __init__(self, version=""):
        super().__init__()
        self._version = version
        self.__os_name = OSManager().get_os_name

    @property
    def reg(self):
        """
        获取reg命令路径
        :return:
        """
        if self.__os_name == OSType.WIN:
            reg = rf'{os.getenv("SystemRoot")}\System32\reg.exe'  # 拼接reg命令完整路径，避免报错
            if not os.path.exists(reg):
                raise FileNotFoundError(f'当前Windows环境没有该命令: {reg}')
            return reg

    def cmd_dict(self, client):
        """
        根据不同操作系统、不同客户端，返回获取版本号的命令、正则表达式
        :param client:
        :return:
        """
        self.log.debug(f'当前OS: {self.__os_name}')
        cmd_map = {
            OSType.MAC: {
                ClientType.Chrome: r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
                ClientType.Firefox: r"/Applications/Firefox.app/Contents/MacOS/firefox --version",
                ClientType.Edge: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version',
            },
            OSType.WIN: {
                ClientType.Chrome: fr'{self.reg} query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                ClientType.Firefox: fr'{self.reg} query "HKEY_CURRENT_USER\Software\Mozilla\Mozilla Firefox" /v CurrentVersion',
                ClientType.Edge: fr'{self.reg} query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version',
            },
            OSType.LINUX: {
                ClientType.Chrome: "google-chrome --version",
                ClientType.Firefox: "firefox --version",
                ClientType.Edge: "microsoft-edge --version",
            },
        }
        cmd = cmd_map[self.__os_name][client]
        client_pattern = CLIENT_PATTERN[client]
        self.log.debug(f'执行命令: {cmd}, 解析方式: {client_pattern}')
        return cmd, client_pattern

    @staticmethod
    def __read_version_from_cmd(cmd, pattern):
        """
        执行命令，并根据传入的正则表达式，获取到正确的版本号
        :param cmd:
        :param pattern:
        :return:
        """
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                shell=True,
        ) as stream:
            stdout = stream.communicate()[0].decode()
            version = re.search(pattern, stdout)
            version = version.group(0) if version else None
        return version

    def get_version(self, client):
        """
        获取指定浏览器版本
        如果当前类的属性中有版本号，则直接返回目标版本号
        :param client:
        :return:
        """
        if not self._version:
            self._version = self.__read_version_from_cmd(*self.cmd_dict(client))
            self.log.info(f'获取本地浏览器版本: {client} - {self._version}')
        return self._version

    def get_chrome_correct_version(self, version=None):
        """
        获取chrome版本对应的chromedriver版本，如果没有对应的chromedriver版本，则模糊向下匹配一个版本
        :return:
        """
        self._version = version if version else self.get_version(ClientType.Chrome)
        # self.get_version(ClientType.Chrome)
        return self._get_chrome_correct_version()

    @staticmethod
    def get_chrome_latest_version(flag='Stable'):
        """
        获取最新版本的ChromeDriver版本
        :param flag: Stable、Beta、Dev、Canary
        :return:
        """
        assert flag in ['Stable', 'Beta', 'Dev', 'Canary'], '参数异常！'
        return request_get(config.ChromeDriverLastVersion).json()['channels'][flag]['version']

    @property
    def get_geckodriver_version(self):
        """
        获取Firefox driver版本信息
        :return:
        """
        return request_get(config.GeckodriverApiNew).json()["latest"]
