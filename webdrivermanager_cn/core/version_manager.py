"""
搜索版本，如果版本不存在，则找比当前小一版本
"""
import re
import subprocess

import requests
from packaging import version as vs

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.os_manager import OSManager, OSType


class ClientType:
    Chrome = "google-chrome"
    Chromium = "chromium"
    Edge = "edge"
    Firefox = "firefox"
    Safari = "safari"


CLIENT_PATTERN = {
    ClientType.Chrome: r"\d+\.\d+\.\d+.\d+",
    ClientType.Firefox: r"\d+\.\d+\.\d+",
    ClientType.Edge: r"\d+\.\d+\.\d+.\d+",
}


class GetUrl:
    """
    根据版本获取url
    """

    def __init__(self):
        self._version = ""

    @property
    def _version_obj(self):
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
        return self._version_obj.major >= 115

    @property
    def get_host(self):
        """
        根据判断获取chromedriver的url
        :return:
        """
        if self.is_new_version:
            return config.ChromeDriverUrlNew
        else:
            return config.ChromeDriverUrl

    @property
    def _version_list(self):
        """
        解析driver url，获取所有driver版本
        :return:
        """
        return [i["name"].replace("/", "") for i in requests.get(self.get_host).json()]

    def _get_chrome_correct_version(self):
        """
        根据传入的版本号，判断是否存在，如果不存在，则返回与它最近的小一版本
        :return:
        """
        return self.__compare_versions(self._version, self._version_list)

    @staticmethod
    def __compare_versions(target_version, version_list):
        """
        根据目标version检查并获取版本
        如果当前版本在版本列表中，则直接返回列表，否则返回当前版本小的一个版本
        :param target_version:
        :param version_list:
        :return: version
        """
        if target_version not in version_list:
            lesser_version = None
            for version in version_list:
                if version < target_version:
                    lesser_version = version
                else:
                    break
            return lesser_version
        return target_version


class GetClientVersion(GetUrl):
    """
    获取当前环境下浏览器版本
    """

    def __init__(self, version=""):
        super().__init__()
        self._version = version

    @staticmethod
    def cmd_dict(client):
        """
        根据不同操作系统、不同客户端，返回获取版本号的命令、正则表达式
        :param client:
        :return:
        """
        os_type = OSManager().get_os_name
        cmd_map = {
            OSType.MAC: {
                ClientType.Chrome: "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
                ClientType.Firefox: r"/Applications/Firefox.app/Contents/MacOS/firefox --version",
                ClientType.Edge: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version'
            },
            OSType.WIN: {
                ClientType.Chrome: 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            },
            OSType.LINUX: {
                ClientType.Chrome: "google-chrome --version",
            },
        }
        return cmd_map[os_type][client], CLIENT_PATTERN[client]

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
        return self._version

    def get_chrome_correct_version(self, version):
        """
        获取chrome版本对应的chromedriver版本
        如果传入的chrome版本没有对应的chromedriver版本，则模糊向下匹配一个版本
        :param version:
        :return:
        """
        self._version = version
        return self._get_chrome_correct_version()

    def get_geckodriver_version(self):
        if self._version:
            return self._version
        url = f"{config.GeckodriverApi}/latest"
        response = requests.get(url=url)
        return response.json()["tag_name"]
