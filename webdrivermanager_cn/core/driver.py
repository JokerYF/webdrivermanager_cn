"""
Driver抽象类
"""
import abc
import datetime
import os.path

from packaging import version as vs
from requests import HTTPError

from webdrivermanager_cn.core.download_manager import DownloadManager
from webdrivermanager_cn.core.driver_cache import DriverCacheManager
from webdrivermanager_cn.core.file_manager import FileManager


class DriverManager(metaclass=abc.ABCMeta):
    """
    Driver基类
    """

    def __init__(self, driver_name, version, root_dir):
        """
        Driver基类
        :param driver_name: Driver名称
        :param version: Driver版本
        :param root_dir: 缓存文件地址
        """
        self.driver_name = driver_name
        self.version = version
        self.__cache_manager = DriverCacheManager(root_dir=root_dir)
        self.__driver_path = os.path.join(
            self.__cache_manager.root_dir, self.driver_name, self.version
        )

    @property
    def version_parse(self):
        """
        版本号解析器
        :return:
        """
        return vs.parse(self.version)

    def get_cache(self):
        """
        获取cache信息
        根据driver名称，版本号为key获取对应的driver路径
        :return: path or None
        """
        return self.__cache_manager.get_cache(
            driver_name=self.driver_name, version=self.version
        )

    def __set_cache(self, path):
        """
        写入cache信息
        :param path: 解压后的driver全路径
        :return: None
        """
        self.__cache_manager.set_cache(
            driver_name=self.driver_name,
            update=f"{datetime.datetime.today()}",
            path=path,
            version=self.version,
        )

    @abc.abstractmethod
    def download_url(self) -> str:
        """
        获取文件下载url
        抽象接口方法，继承时需要重写
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    @abc.abstractmethod
    def get_driver_name(self) -> str:
        """
        获取driver压缩包名称
        抽象接口方法，继承时需要重写
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    @abc.abstractmethod
    def get_os_info(self):
        """
        获取操作系统信息
        抽象接口方法，继承时需要重写
        :return:
        """
        raise NotImplementedError("该方法需要重写")

    def download(self) -> str:
        """
        文件下载、解压
        :return: abs path
        """
        url = self.download_url()
        download_path = DownloadManager().download_file(url, self.__driver_path)
        file = FileManager(download_path, self.driver_name)
        file.unpack()
        return file.driver_path()

    def install(self) -> str:
        """
        获取webdriver路径
        如果webdriver对应缓存存在，则返回文件路径
        如果不存在，则下载、解压、写入缓存，返回路径
        :raise: Exception，如果下载版本不存在，则会报错
        :return: abs path
        """
        driver_path = self.get_cache()
        if not driver_path:
            try:
                driver_path = self.download()
            except HTTPError:
                raise Exception(f"无版本: {self.driver_name} - {self.version}")
            self.__set_cache(driver_path)
        os.chmod(driver_path, 0o755)
        return driver_path
