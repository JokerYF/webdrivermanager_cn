"""
文件管理
"""
import os.path
import tarfile
import zipfile

from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.os_manager import OSManager, OSType


class FileManager(LogMixin):
    """
    文件管理、解压、获取driver路径
    """

    def __init__(self, file_path, driver_name):
        """
        文件管理
        :param file_path:
        :param driver_name:
        """
        self.__driver_name = driver_name
        self.__unpack_path = None
        self.__path = file_path
        self.__unpack_obj = UnpackManager(self.__path)

    @property
    def file_name(self):
        """
        获取文件名
        :return:
        """
        return os.path.basename(self.__path)

    @property
    def dir_path(self):
        """
        获取文件父路径
        :return:
        """
        return os.path.dirname(self.__path)

    def unpack(self):
        """
        文件解压缩
        :return:
        """
        self.__unpack_path = self.__unpack_obj.unpack()
        self.log.debug(f'文件解压路径: {self.__unpack_path}')

    def unpack_list(self):
        """
        获取解压缩后的文件列表（全路径）
        :return:
        """
        file_list = []
        for root, folder, file in os.walk(self.__unpack_path):
            for file_name in file:
                file_list.append(os.path.join(root, file_name))
        return file_list

    @property
    def driver_path(self):
        """
        获取 webdriver 路径
        :return:
        """
        suffix = ''
        if self.__driver_name == "edgedriver":
            self.__driver_name = "msedgedriver"
        if OSManager().get_os_name == OSType.WIN:
            suffix = '.exe'
        driver_name = self.__driver_name + suffix
        for i in self.unpack_list():
            if driver_name == os.path.basename(i):
                return i


class UnpackManager:
    """
    文件解压缩管理器
    """

    def __init__(self, path):
        """
        文件解压缩
        :param path:
        """
        self.__path = path

    @property
    def is_zip_file(self):
        """
        判断压缩包是否为zip文件
        :return:
        """
        return zipfile.is_zipfile(self.__path)

    @property
    def is_tar_file(self):
        """
        判断压缩包是否为tar文件
        :return:
        """
        return tarfile.is_tarfile(self.__path)

    @property
    def __to_dir(self):
        """
        获取文件解压后的路径
        :return:
        """
        file_name = os.path.basename(self.__path)
        if self.is_zip_file:
            file_name = file_name.replace('.zip', '')
        elif self.is_tar_file:
            file_name = file_name.replace('.tar.gz', '')
        else:
            file_name = file_name.split('.')[0]
        return os.path.join(os.path.dirname(self.__path), file_name)

    @property
    def __unpack_obj(self):
        """
        根据文件压缩包类型，获取对应的解压缩对象
        :return:
        """
        if self.is_zip_file:
            return zipfile.ZipFile
        elif self.is_tar_file:
            return TarFile

    def unpack(self) -> str:
        """
        文件解压缩，并返回解压缩后的路径
        :return:
        """
        self.__unpack_obj(self.__path).extractall(self.__to_dir)
        return self.__to_dir


class TarFile:
    """
    tar文件解压的二次封装
    """

    def __init__(self, file_path):
        self.__file_path = file_path

    def extractall(self, to_dir):
        try:
            tar = tarfile.open(self.__file_path, mode="r:gz")
        except tarfile.TarError:
            tar = tarfile.open(self.__file_path, mode="r:bz2")
        tar.extractall(to_dir)
        tar.close()
