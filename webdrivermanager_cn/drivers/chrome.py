from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.log_manager import wdm_logger
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion


class ChromeDriver(DriverManager):
    def __init__(self, version='latest', path=None):
        self._chromedriver_version = version
        super().__init__(driver_name='chromedriver', version=self._version, root_dir=path)

    @property
    def get_driver_name(self):
        _name = f"chromedriver-{self.get_os_info()}.zip"
        return _name if self.__is_new_version(self._chromedriver_version) else _name.replace('-', '_')

    def __is_new_version(self, version) -> bool:
        """
        判断是否为新Chrome版本
        :return:
        """
        try:
            return self.version_parse(version).major >= 115
        except:
            return True

    def download_url(self):
        if self.__is_new_version(self._version):
            url = f'{config.ChromeDriverUrlNew}/{self.driver_version}/{self.get_os_info()}/{self.get_driver_name}'
        else:
            url = f'{config.ChromeDriverUrl}/{self.driver_version}/{self.get_driver_name}'
        wdm_logger().debug(f'拼接下载url: {url}')
        return url

    @property
    def _version(self):
        """
        获取当前系统内chrome的版本，并模糊匹配当前版本最高版本的ChromeDriver，否则返回指定的ChromeDriver版本
        :return:
        """
        if self._chromedriver_version == 'latest':
            try:
                return GetClientVersion().get_chrome_correct_version()
            except:
                return GetClientVersion().get_chrome_latest_version()
        return self._chromedriver_version

    def get_os_info(self, mac_format=True):
        _os_type = f"{self.os_info.get_os_type}{self.os_info.get_framework}"
        if self.os_info.get_os_name == OSType.MAC:
            if mac_format:
                mac_suffix = self.os_info.get_mac_framework
                if mac_suffix and mac_suffix in _os_type:
                    return "mac-arm64"
                else:
                    return "mac-x64"
        elif self.os_info.get_os_name == OSType.WIN:
            if not GetClientVersion(self.driver_version).is_new_version:
                return 'win32'
        return _os_type
