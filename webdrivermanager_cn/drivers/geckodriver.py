"""
Firefox 浏览器驱动
"""
from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSManager, OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion


class Geckodriver(DriverManager):
    def __init__(self, version=None, path=None):
        self.__os_manager = OSManager()
        if not version:
            version = GetClientVersion().get_geckodriver_version()
        super().__init__(driver_name='geckodriver', version=version, root_dir=path)

    def download_url(self):
        return f'{config.GeckodriverUrl}/{self.version}/{self.get_driver_name()}'

    def get_driver_name(self) -> str:
        pack_type = 'zip' if self.__os_manager == OSType.WIN else 'tar.gz'
        return f'{self.driver_name}-{self.version}-{self.get_os_info()}.{pack_type}'

    def get_os_info(self):
        _os_type_suffix = self.__os_manager.get_os_architecture
        _os_type = self.__os_manager.get_os_name

        if self.__os_manager.is_aarch64:
            _os_type_suffix = '-aarch64'
        elif _os_type == OSType.MAC:
            _os_type_suffix = ''

        if _os_type == OSType.MAC:
            _os_type = 'macos'

        return f'{_os_type}{_os_type_suffix}'
