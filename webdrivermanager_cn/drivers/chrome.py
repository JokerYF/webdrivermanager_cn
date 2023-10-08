import requests
from packaging import version as vs
from requests import HTTPError

from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSManager, OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion


class ChromeDriver(DriverManager):
    def __init__(self, version='latest', path=None):
        self._chromedriver_version = version
        super().__init__(driver_name='chromedriver', version=self._version, root_dir=path)

    def get_driver_name(self):
        if GetClientVersion(self.driver_version).is_new_version:
            return f"{self.get_os_info()}/chromedriver-{self.get_os_info()}.zip"
        return f"chromedriver_{self.get_os_info()}.zip".replace('-', '_')

    def download_url(self):
        """
        获取driver的下载url
        :return:
        """
        if self.version_parse.major <= 114:
            host = config.ChromeDriverUrl
        else:
            host = config.ChromeDriverUrlNew

        url = f'{host}/{self.driver_version}/{self.get_driver_name()}'
        return url

    def __get_latest_release(self):
        try:
            version_parser = vs.parse(self._chromedriver_version)
        except:
            version_parser = 'STABLE'
        params = f'LATEST_RELEASE_{version_parser}'
        url = f'{config.ChromeDriver}/{params}'
        response = requests.get(url)
        return response.text

    @property
    def _version(self):
        """
        优先通过ChromeDriver官方url获取最新版本，如果失败，则获取本地chrome版本后模糊匹配
        :return:
        """
        if self._chromedriver_version == 'latest' or self._chromedriver_version:
            try:
                return self.__get_latest_release()
            except HTTPError:
                pass
        return GetClientVersion().get_chrome_correct_version()

    def get_os_info(self, os_type=None, mac_format=True):
        """
        格式化操作系统类型
        用于拼接下载url相关信息
        :param os_type:
        :param mac_format:
        :return:
        """
        os_info = OSManager()

        if os_type:
            return os_type
        _os_type = f"{os_info.get_os_type}{os_info.get_framework}"
        if os_info.get_os_name == OSType.MAC:
            if mac_format:
                mac_suffix = os_info.get_mac_framework
                if mac_suffix and mac_suffix in _os_type:
                    return "mac-arm64"
                else:
                    return "mac-x64"
        elif os_info.get_os_name == OSType.WIN:
            if not GetClientVersion(self.driver_version).is_new_version:
                return 'win32'
        return _os_type
