"""
Driver抽象类
"""
import abc
import os.path

from packaging import version as vs
from requests import RequestException

from webdrivermanager_cn.core.cache_manager import DriverCacheManager
from webdrivermanager_cn.core.download_manager import DownloadManager
from webdrivermanager_cn.core.file_manager import FileManager
from webdrivermanager_cn.core.mixin import EnvMixin
from webdrivermanager_cn.core.os_manager import OSManager
from webdrivermanager_cn.core.time_ import get_time


class DriverManager(EnvMixin, metaclass=abc.ABCMeta):
    """
    Driver抽象类
    不能实例化，只能继承并重写抽象方法
    """

    def __init__(self, driver_name, version, root_dir):
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
            self.driver_version
        )
        self.log.info(f'获取WebDriver: {self.driver_name} - {self.driver_version}')

    @staticmethod
    def version_parse(version):
        """
        版本号解析器
        :return:
        """
        return vs.parse(version)

    def get_driver_path_by_cache(self):
        """
        获取 cache 中对应 WebDriver 的路径
        :return: path or None
        """

        path = self.get_env

        if not path:
            path = self.__cache_manager.get_cache(
                driver_name=self.driver_name,
                version=self.driver_version,
                key='path',
            )
            if path:
                self.set_env(path)

        return path

    @property
    def __env_key(self):
        return f'{self.driver_name}_{self.driver_version}'

    @property
    def get_env(self):
        return self.get(self.__env_key)

    def set_env(self, path):
        self.set(self.__env_key, path)

    # @property
    # def get_last_read_by_cache(self):
    #     """
    #     获取 cache 中对应 WebDriver 的路径
    #     :return: path or None
    #     """
    #     return self.__cache_manager.get_cache(
    #         driver_name=self.driver_name,
    #         version=self.driver_version,
    #         key='last_read_time',
    #     )

    def __set_cache(self, path):
        """
        写入cache信息
        :param path: 解压后的driver全路径
        :return: None
        """
        self.__cache_manager.set_cache(driver_name=self.driver_name, version=self.driver_version,
                                       download_time=f"{get_time('%Y%m%d')}", path=path)

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
                driver_path = self.download()
            except RequestException as e:
                raise Exception(f"下载WebDriver: {self.driver_name}-{self.driver_version} 失败！-- {e}")
            self.__set_cache(driver_path)
            self.set_env(driver_path)

            # 写入读取时间，并清理超期 WebDriver
            self.__cache_manager.set_read_cache_date(self.driver_name, self.driver_version)
            self.__cache_manager.clear_cache_path(self.driver_name)

        # self.log.info(f'WebDriver路径: {driver_path} - 上次读取时间 {self.get_last_read_by_cache}')
        os.chmod(driver_path, 0o755)

        return driver_path
