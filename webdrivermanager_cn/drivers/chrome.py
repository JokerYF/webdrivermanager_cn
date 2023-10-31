import requests
from packaging import version as vs
from requests import HTTPError

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.log_manager import wdm_logger
from webdrivermanager_cn.core.os_manager import OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion, ClientType


class ChromeDriver(DriverManager):
    def __init__(self, version='latest', path=None):
        self._chromedriver_version = version
        super().__init__(driver_name='chromedriver', version=self._version, root_dir=path)

    @property
    def get_driver_name(self):
        if GetClientVersion(self.driver_version).is_new_version:
            return f"chromedriver-{self.get_os_info()}.zip"
        return f"chromedriver_{self.get_os_info()}.zip".replace('-', '_')

    @property
    def __is_new_version(self) -> bool:
        """
        判断是否为新Chrome版本
        :return:
        """
        try:
            return vs.parse(self._chromedriver_version).major >= 115
        except:
            return True

    def download_url(self):
        if self.__is_new_version:
            url = f'{config.ChromeDriverUrlNew}/{self.driver_version}/{self.get_os_info()}/{self.get_driver_name}'
        else:
            url = f'{config.ChromeDriverUrl}/{self.driver_version}/{self.get_driver_name}'
        wdm_logger().debug(f'拼接下载url: {url}')
        return url

    def __get_latest_release_version(self, version=None):
        """
        通过GitHub获取ChromeDriver最新版本号
        :return:
        """
        host = config.ChromeDriver
        if not version:
            version = self._chromedriver_version

        if version == 'latest':
            version = 'STABLE'
        else:
            version_parser = vs.parse(version)
            version = f'{version_parser.major}.{version_parser.minor}.{version_parser.micro}'
            if not self.__is_new_version:
                host = config.ChromeDriverUrl
        url_params = f'LATEST_RELEASE_{version}'
        wdm_logger().debug(f'获取 ChromeDriver {url_params}')
        url = f'{host}/{url_params}'
        response = requests.get(url)
        wdm_logger().debug(f'{url} - {response.status_code}')
        response.raise_for_status()
        return response.text

    @property
    def _version(self):
        """
        优先通过ChromeDriver官方url获取最新版本，如果失败，则获取本地chrome版本后模糊匹配
        :return:
        """
        if self._chromedriver_version and self._chromedriver_version != 'latest':
            return self._chromedriver_version
        elif self._chromedriver_version == 'latest':
            try:
                return self.__get_latest_release_version()
            except HTTPError:
                pass
        version = GetClientVersion().get_version(ClientType.Chrome)
        try:
            return self.__get_latest_release_version(version)
        except HTTPError:
            return GetClientVersion().get_chrome_correct_version()

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
        wdm_logger().debug(f'操作系统信息: {self.driver_name} - {_os_type}')
        return _os_type
