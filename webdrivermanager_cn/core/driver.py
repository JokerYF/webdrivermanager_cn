"""
Driver抽象类
"""
import abc
import os.path

from requests import RequestException

from webdrivermanager_cn.core.cache_manager import DriverCacheManager, CacheLock
from webdrivermanager_cn.core.download_manager import DownloadManager
from webdrivermanager_cn.core.file_manager import FileManager
from webdrivermanager_cn.core.mirror_manager import ChromeDriverMirror, MirrorType, GeckodriverMirror, EdgeDriverMirror
from webdrivermanager_cn.core.mixin import EnvMixin
from webdrivermanager_cn.core.os_manager import OSManager
from webdrivermanager_cn.core.time_ import get_time
from webdrivermanager_cn.core.version_manager import VersionManager


class DriverType:
    chrome = 'chromedriver'
    firefox = 'geckodriver'
    edge = 'msedgedriver'


class DriverManager(EnvMixin, metaclass=abc.ABCMeta):
    """
    Driver抽象类
    不能实例化，只能继承并重写抽象方法
    """

    def __init__(self, driver_name, version, root_dir, mirror_type=None):
        """
        Driver基类
        :param driver_name: Driver名称
        :param version: Driver版本
        :param root_dir: 缓存文件地址
        """
        self.driver_name = driver_name
        self.driver_version = version
        self.os_info = OSManager()
        self.__cache_manager = DriverCacheManager(root_dir=root_dir)
        self.__driver_path = os.path.join(
            self.__cache_manager.root_dir,
            self.driver_name,
            self.download_version
        )
        self.__cache_manager.driver_version = self.driver_version
        self.__cache_manager.driver_name = self.driver_name
        self.__cache_manager.download_version = self.download_version
        self.__mirror_type = mirror_type
        # self.log.info(f'获取WebDriver: {self.driver_name} - {self.download_version}')

    @property
    def mirror_type(self):
        if not self.__mirror_type:
            self.__mirror_type = MirrorType.Ali
        return self.__mirror_type

    @mirror_type.setter
    def mirror_type(self, value):
        self.__mirror_type = value

    def get_driver_path_by_cache(self):
        """
        获取 cache 中对应 WebDriver 的路径
        :return: path or None
        """
        _path = self.__cache_manager.get_cache(key='path')
        if _path and os.path.exists(_path):
            self.__cache_manager.set_read_cache_date()
            return _path
        return None

    @property
    def mirror(self):
        if self.driver_name == DriverType.chrome:
            return ChromeDriverMirror(mirror_type=self.mirror_type)
        elif self.driver_name == DriverType.firefox:
            return GeckodriverMirror(mirror_type=self.mirror_type)
        elif self.driver_name == DriverType.edge:
            return EdgeDriverMirror(mirror_type=self.mirror_type)

    def __set_cache(self, path):
        """
        写入cache信息
        :param path: 解压后的driver全路径
        :return: None
        """
        self.__cache_manager.set_cache(
            version=self.download_version,
            download_time=f"{get_time('%Y%m%d')}",
            path=path,
        )
        self.__cache_manager.set_read_cache_date()

    @property
    @abc.abstractmethod
    def download_url(self) -> str:
        """
        获取文件下载url
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    @property
    @abc.abstractmethod
    def get_driver_name(self) -> str:
        """
        获取driver压缩包名称
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    @property
    @abc.abstractmethod
    def get_os_info(self):
        """
        获取操作系统信息
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    @property
    def download_version(self):
        return self.version_manager.download_version

    @property
    @abc.abstractmethod
    def version_manager(self) -> VersionManager:
        raise NotImplementedError("该方法需要重写")

    def download(self) -> str:
        """
        文件下载、解压
        :return: abs path
        """
        download_path = DownloadManager().download_file(self.download_url, self.__driver_path)
        file = FileManager(download_path, self.driver_name)
        file.unpack()
        return file.driver_path

    def install(self) -> str:
        """
        获取webdriver路径
        如果webdriver对应缓存存在，则返回文件路径
        如果不存在，则下载、解压、写入缓存，返回路径
        :raise: Exception，如果下载版本不存在，则会报错
        :return: abs path
        """
        driver_path = self.get_driver_path_by_cache()
        if not driver_path:
            self.log.info('缓存不存在，开始下载...')
            try:
                with CacheLock(self.__cache_manager.root_dir):
                    driver_path = self.download()
                    self.__set_cache(driver_path)
            except RequestException as e:
                raise Exception(f"下载WebDriver: {self.driver_name}-{self.download_version} 失败！-- {e}")
            self.__cache_manager.clear_cache_path()

        os.chmod(driver_path, 0o755)
        self.log.info(f'获取 {self.driver_name} - {self.download_version} - {driver_path}')

        return driver_path
