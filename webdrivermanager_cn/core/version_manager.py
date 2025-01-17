import os
import re
import subprocess
from abc import ABC, abstractmethod

from packaging import version as vs

from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.mirror_manager import ChromeDriverMirror, MirrorType, GeckodriverMirror
from webdrivermanager_cn.core.mixin import Env
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


class GetClientVersion(LogMixin):
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
        self.log.debug(f'当前OS: {self.os_type} 执行命令: {cmd}, 解析方式: {client_pattern}')
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
        return version.group(0) if version else None

    def get_version(self, client):
        """
        获取指定浏览器版本
        如果当前类的属性中有版本号，则直接返回目标版本号
        :param client:
        :return:
        """
        _version = self.__read_version_from_cmd(*self.cmd_dict(client))
        self.log.debug(f'获取本地浏览器版本: {client} - {_version}')
        return _version


class VersionManager(ABC):
    def __init__(self, version="", mirror_type: MirrorType = None):
        self.__version = version
        self.__mirror_type = mirror_type

    @property
    def driver_version(self):
        return self.__version if self.__version else "latest"

    @driver_version.setter
    def driver_version(self, version):
        self.__version = version

    @property
    def mirror_type(self):
        return self.__mirror_type

    @property
    @abstractmethod
    def download_version(self):
        raise NotImplementedError('该方法需要重写')

    @property
    @abstractmethod
    def mirror(self):
        raise NotImplementedError('该方法需要重写')

    @staticmethod
    def version_parser(version):
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
        env = Env()
        if not env.get(self.client_type):
            env.set(self.client_type, GetClientVersion().get_version(self.client_type))
        _version = env.get(self.client_type)
        return _version if _version and _version.lower() != 'none' else None

    @property
    def is_new_version(self):
        return


class ChromeDriverVersionManager(VersionManager, GetClientVersion):
    def __init__(self, version="", mirror_type: MirrorType = None):
        super().__init__(version, mirror_type)

    @property
    def client_type(self):
        return ClientType.Chrome

    @property
    def mirror(self):
        return ChromeDriverMirror(self.mirror_type)

    @property
    def mirror_host(self):
        return self.mirror.mirror_url(self.is_new_version)

    @property
    def __get_effective_version(self):
        # 这里只解析传入的版本信息或者本地版本信息，获取失败则返回None
        _version = self.driver_version
        if _version == 'latest':
            _version = self.get_local_version
        return _version

    @property
    def download_version(self):
        _version = self.__get_effective_version
        if not _version:
            return self.latest_version
        return self.__correct_version(_version)

    @property
    def is_new_version(self):
        _version = self.__get_effective_version
        if not _version:
            return True
        return self.version_parser(_version).major >= 115

    @property
    def latest_version(self):
        return request_get(self.mirror.latest_version_url).json()['channels']['Stable']['version']

    @property
    def __version_list(self):
        """
        解析driver url，获取所有driver版本
        :return:
        """
        response_data = request_get(self.mirror_host).json()
        return [i["name"].replace("/", "") for i in response_data if 'LATEST' not in i]

    def __correct_version(self, version):
        _parser = self.version_parser(version)
        _chrome_version = f'{_parser.major}.{_parser.minor}.{_parser.micro}'

        if _parser.major >= 115:
            # 根据json获取符合版本的版本号
            _url = self.mirror.latest_past_version_url
            try:
                data = request_get(_url).json()
                return data['builds'][_chrome_version]['version']
            except KeyError:
                self.log.warning(
                    f'当前chrome版本: {_chrome_version}, '
                    f'没有找到合适的ChromeDriver版本 - {_url}'
                )
        # 拉取符合版本list并获取最后一个版本号
        _chrome_version_list = [i for i in self.__version_list if _chrome_version in i and 'LATEST' not in i]
        _chrome_version_list = sorted(_chrome_version_list, key=lambda x: tuple(map(int, x.split('.'))))
        return _chrome_version_list[-1]


class GeckodriverVersionManager(GetClientVersion, VersionManager):
    def __init__(self, version="", mirror_type: MirrorType = None):
        super().__init__(version, mirror_type)

    @property
    def mirror(self):
        return GeckodriverMirror(self.mirror_type)

    @property
    def download_version(self):
        if self.driver_version and self.driver_version != "latest":
            if not self.driver_version.startswith('v'):
                self.driver_version = f'v{self.driver_version}'
            return self.driver_version
        return self.latest_version

    @property
    def client_type(self):
        return ClientType.Firefox

    @property
    def latest_version(self):
        data = request_get(self.mirror.latest_version_url).json()
        return list(data['geckodriver'].keys())[0]
