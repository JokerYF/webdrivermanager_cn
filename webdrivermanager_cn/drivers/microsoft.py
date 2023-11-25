import requests

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion, ClientType


class EdgeDriverManager(DriverManager):
    def __init__(self, version=None, path=None):
        super().__init__(driver_name="edgedriver", version="", root_dir=path)
        self.driver_version = version if version else self.get_version()

    def get_driver_name(self) -> str:
        return f"{self.driver_name}_{self.get_os_info()}.zip"

    def get_os_info(self):
        _os_info = self.os_info.get_os_type
        if self.os_info.get_mac_framework in ["_m1", "_m2"]:
            _os_info += "_m1"
        return _os_info

    def download_url(self) -> str:
        return f"{config.EdgeDriverUrl}/{self.driver_version}/{self.get_driver_name()}"

    def get_version(self, version=None):
        """
        获取edge driver版本
        :param version:
        :return:
        """
        if version:
            return version

        client_version = GetClientVersion().get_version(ClientType.Edge)
        client_version_parser = GetClientVersion(client_version)
        _os_name = self.os_info.get_os_name
        if _os_name == OSType.WIN:
            suffix = "windows"
        elif _os_name == OSType.MAC:
            suffix = "macos"
        else:
            suffix = OSType.LINUX
        latest_url = f"{config.EdgeDriverUrl}/LATEST_RELEASE_{client_version_parser._version_obj.major}_{suffix.upper()}"
        response = requests.get(latest_url)
        return response.text.strip()
