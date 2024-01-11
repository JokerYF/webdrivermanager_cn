"""
Firefox 浏览器驱动
"""
from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion


class Geckodriver(DriverManager):
    def __init__(self, version=None, path=None):
        if not version:
            version = GetClientVersion().get_geckodriver_version()
        super().__init__(driver_name='geckodriver', version=version, root_dir=path)

    def download_url(self):
        return f'{config.GeckodriverUrl}/{self.driver_version}/{self.get_driver_name}'

    @property
    def get_driver_name(self) -> str:
        pack_type = 'zip' if self.os_info.get_os_name == OSType.WIN else 'tar.gz'
        return f'{self.driver_name}-{self.driver_version}-{self.get_os_info}.{pack_type}'

    @property
    def get_os_info(self):
        _os_type_suffix = self.os_info.get_os_architecture
        _os_type = self.os_info.get_os_name

        if self.os_info.is_aarch64:
            _os_type_suffix = '-aarch64'
        elif _os_type == OSType.MAC:
            _os_type_suffix = ''

        if _os_type == OSType.MAC:
            _os_type = 'macos'

        return f'{_os_type}{_os_type_suffix}'
