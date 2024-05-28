from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.request import request_get
from webdrivermanager_cn.core.version_manager import GetClientVersion, ClientType


class EdgeDriver(DriverManager):
    def __init__(self, version=None, path=None):
        super().__init__(driver_name="edgedriver", version="", root_dir=path)
        self.driver_version = self.get_version(version)  # edge 官方没有latest的url，只能根据本地版本获取

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
        根据传入版本，或者自动获取的Edge版本，获取匹配的webdriver版本
        :param version:
        :return:
        """
        if version and version != 'latest':
            client_version = version
        else:
            client_version = GetClientVersion().get_version(ClientType.Edge)
        client_version_parser = GetClientVersion(client_version)
        _os_name = self.os_info.get_os_name
        if _os_name == OSType.WIN:
            suffix = "windows"
        elif _os_name == OSType.MAC:
            suffix = "macos"
        else:
            suffix = OSType.LINUX
        latest_url = f"{config.EdgeDriverUrl}/LATEST_RELEASE_{client_version_parser.version_obj.major}_{suffix.upper()}"

        return request_get(latest_url).text.strip()
