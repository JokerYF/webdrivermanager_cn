from webdrivermanager_cn.core.driver import DriverManager, DriverType
from webdrivermanager_cn.core.mirror_manager import MirrorType
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.version_manager import VersionManager, GeckodriverVersionManager


class Geckodriver(DriverManager):
    def __init__(self, version='latest', path=None, mirror_type: MirrorType = None):
        super().__init__(
            driver_name=DriverType.firefox,
            version=version,
            root_dir=path,
            mirror_type=mirror_type
        )

    @property
    def version_manager(self) -> VersionManager:
        return GeckodriverVersionManager(self.driver_version)

    @property
    def download_url(self) -> str:
        mirror = self.mirror.mirror_url()
        return f'{mirror}/{self.download_version}/{self.get_driver_name}'

    @property
    def get_driver_name(self) -> str:
        pack_type = 'zip' if self.os_info.is_win else 'tar.gz'
        return f'{self.driver_name}-{self.download_version}-{self.get_os_info}.{pack_type}'

    @property
    def get_os_info(self):
        _os_type_suffix = self.os_info.get_os_architecture
        _os_type = self.os_info.get_os_name

        if self.os_info.is_aarch64:
            _os_type_suffix = '-aarch64'
        elif _os_type == OSType.MAC:
            _os_type_suffix = ''
            _os_type = 'macos'

        return f'{_os_type}{_os_type_suffix}'
