from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSManager, OSType
from webdrivermanager_cn.core.version_manager import GetClientVersion, ClientType


class ChromeDriver(DriverManager):
    def __init__(self, version=None, path=None):
        if not version:
            version = GetClientVersion().get_version(ClientType.Chrome)
        super().__init__(driver_name='chromedriver', version=version, root_dir=path)

    def get_driver_name(self):
        if GetClientVersion(self.version).is_new_version:
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

        url = f'{host}/{self.version}/{self.get_driver_name()}'
        return url

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
            if not GetClientVersion(self.version).is_new_version:
                return 'win32'
        return _os_type
