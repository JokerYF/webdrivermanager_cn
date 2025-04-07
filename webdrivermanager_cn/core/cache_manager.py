"""
Driver 缓存记录
"""
import json
import os
import shutil
from json import JSONDecodeError
from filelock import FileLock

from webdrivermanager_cn.core.config import clear_wdm_cache_time
from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.os_manager import OSManager
from webdrivermanager_cn.core.time_ import get_time


class DriverCacheManager(LogMixin):
    """
    Driver 缓存管理
    """

    def __init__(self, root_dir=None):
        """
        缓存管理
        :param root_dir:
        """
        self.__root_dir = root_dir
        self.__driver_name = None
        self.__driver_version = None
        self.__download_version = None
        self.__lock = FileLock(f'{self.json_path}.lock')

    @property
    def root_dir(self):
        """
        cache文件目录
        :return:
        """
        path = os.path.join(self.__abs_path(self.__root_dir), '.webdriver')
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def json_path(self):
        """
        cache文件目录
        :return:
        """
        return os.path.join(self.root_dir, 'driver_cache.json')

    @staticmethod
    def __abs_path(path):
        """
        返回绝对路径
        :param path:
        :return:
        """
        if not path:
            path = os.path.expanduser('~')
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        return path

    @property
    def driver_version(self):
        """
        返回driver版本
        :return:
        """
        return self.__driver_version

    @driver_version.setter
    def driver_version(self, value):
        self.__driver_version = value

    @property
    def driver_name(self):
        """
        返回driver名称
        :return:
        """
        if not self.__driver_name:
            raise ValueError
        return self.__driver_name

    @driver_name.setter
    def driver_name(self, value):
        self.__driver_name = value

    @property
    def download_version(self):
        """
        返回下载driver版本
        :return:
        """
        if not self.__download_version:
            raise ValueError
        return self.__download_version

    @download_version.setter
    def download_version(self, value):
        self.__download_version = value

    @property
    def os_name(self):
        return OSManager().get_os_name

    @property
    def __json_exist(self):
        """
        判断缓存文件是否存在
        :return:
        """
        return os.path.exists(self.json_path)

    @property
    def __read_cache(self) -> dict:
        """
        读取缓存文件
        :return:
        """
        if not self.__json_exist:
            self.log.debug(f'配置文件不存在: {self.json_path}')
            return {}
        with self.__lock:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except JSONDecodeError:
                    data = None
        _data = data if data else {}
        # self.log.debug(f"缓存文件大小: {os.path.getsize(self.json_path)}")
        return _data

    def __dump_cache(self, data: dict):
        """
        写入缓存
        :param data:
        :return:
        """
        with self.__lock:
            with open(self.json_path, 'w+', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

    def set_cache(self, **kwargs):
        """
        写入缓存文件
        :param kwargs:
        :return:
        """
        data = self.__read_cache
        key = self.key

        self.log.debug(f'即将写入的数据: {self.driver_name} - {key} - {kwargs}')
        if self.driver_name not in data.keys():
            data[self.driver_name] = {}
        if key not in data[self.driver_name].keys():
            data[self.driver_name][key] = {}

        # WebDriver cache 信息内不记录这些字段
        if 'driver_name' in kwargs.keys():
            kwargs.pop('driver_name')

        data[self.driver_name][key].update(kwargs)
        self.__dump_cache(data)

    @staticmethod
    def __format_key(driver_name, os_name, version):
        return f'{driver_name}_{os_name}_{version}'

    @property
    def key(self) -> str:
        """
        格式化缓存 key 名称
        :return:
        """
        return self.__format_key(self.driver_name, self.os_name, self.download_version)

    def get_cache(self, key):
        """
        获取缓存中的 driver 信息
        如果缓存存在，返回 key 对应的 value；不存在，返回 None
        :param key:
        :return:
        """
        if not self.__json_exist:
            return None
        try:
            return self.__read_cache[self.driver_name][self.key][key]
        except KeyError:
            return None

    @property
    def get_clear_version_by_read_time(self):
        """
        获取超过清理时间的 WebDriver 版本
        :return:
        """
        _clear_version = []
        time_interval = clear_wdm_cache_time()
        cache_dist = self.__read_cache.get(self.driver_name, {})
        for driver, info in cache_dist.items():
            _version = info.get('version')
            try:
                read_time = int(info['last_read_time'])
            except (KeyError, ValueError):
                read_time = 0
            if not read_time or int(get_time('%Y%m%d')) - read_time >= time_interval:
                _clear_version.append(_version)
                self.log.debug(f'{self.driver_name} - {_version} 已过期 {read_time}, 即将清理!')
                continue
            self.log.debug(f'{self.driver_name} - {_version} 尚未过期 {read_time}')
        self.log.debug(f'需要清理的driver: {_clear_version}')
        return _clear_version

    def set_read_cache_date(self):
        """
        写入当前读取 WebDriver 的时间
        :return:
        """
        times = get_time('%Y%m%d')
        if self.get_cache(key='last_read_time') != times:
            self.set_cache(last_read_time=f"{times}")
            self.log.debug(f'更新 {self.driver_name} - {self.download_version} 读取时间: {times}')

    def clear_cache_path(self):
        """
        以当前时间为准，清除超过清理时间的 WebDriver 目录
        :return:
        """
        cache_data = self.__read_cache
        need_clear_version = self.get_clear_version_by_read_time

        if not need_clear_version:
            self.log.info(f'{self.driver_name} 没有过期的 WebDriver')
            return

        for version in need_clear_version:
            clear_path = os.path.join(self.root_dir, self.driver_name, version)
            # 清理本地目录
            if os.path.exists(clear_path):
                shutil.rmtree(clear_path)

            # 清理缓存数据
            __key = self.__format_key(self.driver_name, self.os_name, version)
            if __key in cache_data[self.driver_name].keys():
                cache_data[self.driver_name].pop(__key)
            self.log.info(f'清理过期WebDriver: {clear_path}')

        self.__dump_cache(cache_data)
        self.log.info(f'清理过期WebDriver: {self.driver_name} 成功!')
