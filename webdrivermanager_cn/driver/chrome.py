from webdrivermanager_cn.core.driver import DriverManager, DriverType
from webdrivermanager_cn.core.mirror_manager import MirrorType
from webdrivermanager_cn.core.version_manager import ChromeDriverVersionManager


class ChromeDriver(DriverManager):
    def __init__(self, version='latest', path=None, mirror_type: MirrorType = None):
        super().__init__(
            driver_name=DriverType.chrome,
            version=version,
            root_dir=path,
            mirror_type=mirror_type,
        )

    @property
    def download_url(self) -> str:
        mirror = self.mirror.mirror_url(self.download_version)
        if self.mirror.is_huawei or (self.mirror.is_ali and not self.version_manager.is_new_version):
            url = f'{mirror}/{self.download_version}/{self.get_driver_name}'
        else:
            url = f'{mirror}/{self.download_version}/{self.get_os_info}/{self.get_driver_name}'
        self.log.debug(f'拼接下载url {self.mirror_type} - {url}')
        return url

    @property
    def version_manager(self):
        return ChromeDriverVersionManager(version=self.driver_version)

    @property
    def get_driver_name(self) -> str:
        _name = f"chromedriver-{self.get_os_info}.zip"
        return _name if self.version_manager.is_new_version else _name.replace('-', '_')

    @property
    def get_os_info(self):
        _os_type = f"{self.os_info.get_os_type}{self.os_info.get_framework}"
        if self.os_info.is_mac:
            mac_suffix = self.os_info.get_mac_framework
            if mac_suffix and mac_suffix in _os_type:
                return "mac-arm64"
            else:
                return "mac-x64"
        elif self.os_info.is_win:
            if not self.version_manager.is_new_version:
                return 'win32'
        return _os_type
