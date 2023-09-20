import abc
import datetime
import os.path

from packaging import version as vs
from requests import HTTPError

from webdrivermanagercn.core.config import wdm_logger as log
from webdrivermanagercn.core.download_manager import DownloadManager
from webdrivermanagercn.core.driver_cache import DriverCacheManager
from webdrivermanagercn.core.file_manager import FileManager


class DriverManager(metaclass=abc.ABCMeta):
    def __init__(self, driver_name, version, root_dir):
        self.driver_name = driver_name
        self.version = version
        self.__cache_manager = DriverCacheManager(root_dir=root_dir)
        self.__driver_path = os.path.join(self.__cache_manager.root_dir, self.driver_name, self.version)
        log.info(f'{"#" * 20} WebDriverManager {"#" * 20}')

    @property
    def version_parse(self):
        return vs.parse(self.version)

    def get_cache(self):
        return self.__cache_manager.get_cache(
            driver_name=self.driver_name,
            version=self.version
        )

    def __set_cache(self, path):
        self.__cache_manager.set_cache(
            driver_name=self.driver_name,
            update=f'{datetime.datetime.today()}',
            path=path,
            version=self.version
        )

    @abc.abstractmethod
    def download_url(self):
        raise NotImplementedError('该方法需要重写')

    def download(self):
        url = self.download_url()
        download_path = DownloadManager().download_file(url, self.__driver_path)
        file = FileManager(download_path, self.driver_name)
        file.unpack()
        return file.driver_path()

    def install(self):
        driver_path = self.get_cache()
        if not driver_path:
            log.info(f'缓存不存在: {self.driver_name} - {self.version}')
            try:
                driver_path = self.download()
            except HTTPError:
                raise Exception(f'无版本: {self.driver_name} - {self.version}')
            self.__set_cache(driver_path)
        os.chmod(driver_path, 0o755)
        log.info(f'driver 路径: {driver_path}')
        return driver_path
