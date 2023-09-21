import os.path
import tarfile
import zipfile

from webdrivermanagercn.core.os_manager import OSManager, OSType


class FileManager:
    def __init__(self, file_path, driver_name):
        self.__driver_name = driver_name
        self.__unpack_path = None
        self.__path = file_path
        self.__unpack_obj = UnpackManager(self.__path)

    @property
    def file_name(self):
        return os.path.basename(self.__path)

    @property
    def dir_path(self):
        return os.path.dirname(self.__path)

    def unpack(self):
        self.__unpack_path = self.__unpack_obj.unpack()

    def unpack_list(self):
        file_list = []
        for root, folder, file in os.walk(self.__unpack_path):
            for file_name in file:
                file_list.append(os.path.join(root, file_name))
        return file_list

    def driver_path(self):
        suffix = ''
        if OSManager().get_os_name == OSType.WIN:
            suffix = '.exe'
        driver_name = self.__driver_name + suffix
        for i in self.unpack_list():
            if driver_name == os.path.basename(i):
                return i


class UnpackManager:
    def __init__(self, path):
        self.__path = path

    @property
    def is_zip_file(self):
        return zipfile.is_zipfile(self.__path)

    @property
    def is_tar_file(self):
        return tarfile.is_tarfile(self.__path)

    @property
    def __to_dir(self):
        file_name = os.path.basename(self.__path)
        return os.path.join(os.path.dirname(self.__path), file_name.split('.')[0])

    @property
    def __unpack_obj(self):
        if self.is_zip_file:
            return zipfile.ZipFile
        elif self.is_tar_file:
            return TarFile

    def unpack(self):
        self.__unpack_obj(self.__path).extractall(self.__to_dir)
        return self.__to_dir


class TarFile:
    def __init__(self, file_path):
        self.__file_path = file_path

    def extractall(self, to_dir):
        try:
            tar = tarfile.open(self.__file_path, mode="r:gz")
        except tarfile.ReadError:
            tar = tarfile.open(self.__file_path, mode="r:bz2")
        tar.extractall(to_dir)
        tar.close()
