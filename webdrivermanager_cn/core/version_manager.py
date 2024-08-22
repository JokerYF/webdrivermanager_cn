import os
import re
import subprocess
from abc import ABC, abstractmethod

from packaging import version as vs

from webdrivermanager_cn.core.mirror_urls import VersionApi as va
from webdrivermanager_cn.core.os_manager import OSManager, OSType
from webdrivermanager_cn.core.request import request_get


class ClientType:
    Chrome = "google-chrome"
    Edge = "edge"
    Firefox = "firefox"


CLIENT_PATTERN = {
    ClientType.Chrome: r"\d+\.\d+\.\d+\.\d+",
    ClientType.Firefox: r"\d+\.\d+\.\d+",
    ClientType.Edge: r"\d+\.\d+\.\d+\.\d+",
}


class GetClientVersion:
    """
    获取当前环境下浏览器版本
    """

    @property
    def __os_manager(self):
        return OSManager()

    @property
    def os_type(self):
        return self.__os_manager.get_os_name

    @property
    def reg(self):
        """
        获取reg命令路径
        :return:
        """
        if self.os_type == OSType.WIN:
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
        # self.log.debug(f'当前OS: {self.__os_name}')
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
        cmd = cmd_map[self.os_type][client]
        client_pattern = CLIENT_PATTERN[client]
        # self.log.debug(f'执行命令: {cmd}, 解析方式: {client_pattern}')
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
        # self.log.info(f'获取本地浏览器版本: {client} - {self._version}')
        return self.__read_version_from_cmd(*self.cmd_dict(client))


class VersionManager(ABC):
    @staticmethod
    def version_parse(version) -> vs.Version:
        """
        解析版本号
        :param version:
        :return:
        """
        return vs.parse(version)

    @property
    @abstractmethod
    def client_type(self):
        """
        获取客户端类型
        :return:
        """
        raise NotImplementedError('该方法需要重写')

    @property
    @abstractmethod
    def latest_version(self):
        raise NotImplementedError('该方法需要重写')

    @property
    def get_local_version(self):
        return GetClientVersion().get_version(self.client_type)


class ChromeDriverVersionManager(GetClientVersion, VersionManager):
    def __init__(self, version=""):
        self.__version = version

    def client_type(self):
        return ClientType.Chrome

    @property
    def version(self):
        if not self.__version:
            try:
                self.__version = self.get_local_version
            except:
                self.__version = self.latest_version
        return self.__version

    @property
    def is_new_version(self):
        return self.version_parse(self.version).major >= 115

    @property
    def latest_version(self):
        return request_get(va.ChromeDriverApiNew).json()['channels']['Stable']['version']
