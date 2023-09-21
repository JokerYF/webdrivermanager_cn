from webdrivermanagercn.core import config
from webdrivermanagercn.core.driver import DriverManager
from webdrivermanagercn.core.os_manager import OSManager, OSType
from webdrivermanagercn.core.version_manager import GetClientVersion, ClientType


class ChromeDriver(DriverManager):
    def __init__(self, version=None, path=None):
        if not version:
            version = GetClientVersion().get_version(ClientType.Chrome)
        super().__init__(driver_name='chromedriver', version=version, root_dir=path)

    def download_url(self):
        if self.version_parse.major <= 114:
            host = config.ChromeDriverUrl
            params = f"chromedriver_{self.get_os_info()}.zip".replace('-', '_')
        else:
            host = config.ChromeDriverUrlNew
            params = f"{self.get_os_info()}/chromedriver-{self.get_os_info()}.zip"

        url = f'{host}{self.version}/{params}'
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
