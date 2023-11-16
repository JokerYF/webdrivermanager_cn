"""
搜索版本，如果版本不存在，则找比当前小一版本
"""
import os
import re
import subprocess

import requests
from packaging import version as vs

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.log_manager import wdm_logger
from webdrivermanager_cn.core.os_manager import OSManager, OSType


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
        :return: driver_version
        """
        wdm_logger().debug(f'ChromeDriver指定版本: {target_version}')
        if target_version not in version_list:
            lesser_version = None
            for version in version_list:
                if version < target_version:
                    lesser_version = version
                else:
                    break
            wdm_logger().debug(f'当前无该指定版本，最符合的版本为: {lesser_version}')
            return lesser_version
        wdm_logger().debug('当前版本源上存在')
        return target_version


class GetClientVersion(GetUrl):
    """
    获取当前环境下浏览器版本
    """

    def __init__(self, version=""):
        super().__init__()
        self._version = version

    @property
    def reg(self):
        """
        获取reg命令路径
        :return:
        """
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

        os_type = OSManager().get_os_name
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
        cmd = cmd_map[os_type][client]
        client_pattern = CLIENT_PATTERN[client]
        wdm_logger().debug(f'执行命令: {cmd}, 解析方式: {client_pattern}')
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
        wdm_logger().debug('获取到的版本号: %s', version)
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
            wdm_logger().info(f'获取本地浏览器版本: {client} - {self._version}')
        return self._version

    def get_chrome_correct_version(self):
        """
        获取chrome版本对应的chromedriver版本，如果没有对应的chromedriver版本，则模糊向下匹配一个版本
        :return:
        """
        self.get_version(ClientType.Chrome)
        return self._get_chrome_correct_version()

    def get_geckodriver_version(self):
        """
        获取Firefox driver版本信息
        :return:
        """
        if self._version:
            return self._version
        url = f"{config.GeckodriverApi}/latest"
        response = requests.get(url=url)
        return response.json()["tag_name"]
