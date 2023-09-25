"""
Driver 缓存记录
"""
import json
import os

from webdrivermanager_cn.core.os_manager import OSManager


class DriverCacheManager:
    """
    Driver 缓存管理
    """

    def __init__(self, root_dir=None):
        """
        缓存管理
        :param root_dir:
        """
        if not root_dir:
            root_dir = os.path.expanduser('~')
        self.root_dir = os.path.join(root_dir, '.webdriver')
        self.__json_path = os.path.join(self.root_dir, 'driver_cache.json')

    @property
    def __json_exist(self):
        """
        判断缓存文件是否存在
        :return:
        """
        return os.path.exists(self.__json_path)

    def __read_cache(self) -> dict:
        """
        读取缓存文件
        :return:
        """
        if not self.__json_exist:
            return {}
        with open(self.__json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __write_cache(self, **kwargs):
        """
        写入缓存文件
        :param kwargs:
        :return:
        """
        data = self.__read_cache()

        driver_name = kwargs['driver_name']
        version = kwargs['version']
        update = kwargs['update']
        path = kwargs['path']

        if driver_name not in data.keys():
            data[driver_name] = {}
        data[driver_name][self.format_key(driver_name, version)] = {
            'version': version,
            'update': update,
            'path': path,
        }
        with open(self.__json_path, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def format_key(driver_name, version) -> str:
        """
        格式化缓存 key 名称
        :param driver_name:
        :param version:
        :return:
        """
        return f'{driver_name}_{OSManager().get_os_name}_{version}'

    def get_cache(self, driver_name, version):
        """
        获取缓存中的 driver path
        如果缓存存在，返回 path 路径；不存在，返回 None
        :param driver_name:
        :param version:
        :return:
        """
        if not self.__json_exist:
            return None
        try:
            return self.__read_cache()[driver_name][self.format_key(driver_name, version)]['path']
        except KeyError:
            return None

    def set_cache(self, driver_name, version, update, path):
        """
        写入缓存信息
        :param driver_name:
        :param version:
        :param update:
        :param path:
        :return:
        """
        self.__write_cache(
            driver_name=driver_name,
            version=version,
            update=update,
            path=path
        )
