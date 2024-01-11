from webdrivermanager_cn.core import config
from webdrivermanager_cn.core.driver import DriverManager
from webdrivermanager_cn.core.os_manager import OSType


class OpearDriver(DriverManager):
    def __init__(self, version='latest', path=None):
        super().__init__(client_type='operadriver', version=version, root_dir=path)

    def get_driver_name(self) -> str:
        return f'{self.driver_name}_{self.get_os_info()}.zip'

    def get_os_info(self):
        _os_name = self.os_info.get_os_name
        if _os_name == OSType.LINUX:
            return f'{_os_name}64'
        return f'{_os_name}{self.os_info.get_os_architecture}'

    def download_url(self) -> str:
        # https://registry.npmmirror.com/-/binary/operadriver/v.86.0.4240.80/operadriver_win64.zip
        _url = config.OperaDriverUrl

    def _version(self):
        ...
