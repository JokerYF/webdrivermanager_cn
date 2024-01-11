"""
Driver 缓存记录
"""
import json
import os
import shutil
from datetime import datetime

from webdrivermanager_cn.core.config import clear_wdm_cache_time
from webdrivermanager_cn.core.log_manager import wdm_logger
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

    @property
    def __read_cache(self) -> dict:
        """
        读取缓存文件
        :return:
        """
        if not self.__json_exist:
            return {}
        with open(self.__json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __dump_cache(self, data: dict):
        with open(self.__json_path, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def __write_cache(self, **kwargs):
        """
        写入缓存文件
        :param kwargs:
        :return:
        """
        data = self.__read_cache

        driver_name = kwargs['driver_name']
        client_version = kwargs['client_version']
        key = self.format_key(driver_name, client_version)

        if driver_name not in data.keys():
            data[driver_name] = {}
        if key not in data[driver_name].keys():
            data[driver_name][key] = {}

        driver_data = data[driver_name][key]
        for k, v in kwargs.items():
            if k in ['driver_name']:  # WebDriver cache 信息内不记录这些字段
                continue
            driver_data[k] = v
        self.__dump_cache(data)

    @staticmethod
    def format_key(driver_name, client_version) -> str:
        """
        格式化缓存 key 名称
        :param driver_name:
        :param client_version:
        :return:
        """
        return f'{driver_name}_{OSManager().get_os_name}_{client_version}'

    def get_cache(self, driver_name, client_version, key):
        """
        获取缓存中的 driver 信息
        如果缓存存在，返回 key 对应的 value；不存在，返回 None
        :param driver_name:
        :param client_version:
        :param key:
        :return:
        """
        if not self.__json_exist:
            return None
        try:
            driver_key = self.format_key(driver_name, client_version)
            return self.__read_cache[driver_name][driver_key][key]
        except KeyError:
            return None

    def get_cache_path_by_read_time(self, driver_name):
        """
        获取超过清理时间的 WebDriver 版本
        :param driver_name:
        :return:
        """
        path_list = []
        time_interval = 60 * 60 * 24 * clear_wdm_cache_time()
        for driver, info in self.__read_cache[driver_name].items():
            read_time = info.get('last_read_time', None)
            if read_time:
                read_time = datetime.strptime(read_time, '%Y-%m-%d %H:%M:%S.%f')
            if (read_time is None
                    or datetime.today().timestamp() - read_time.timestamp() >= time_interval):
                path_list.append(info['version'])
                wdm_logger().debug(f'{driver_name} 已过期 {read_time}, 即将清理!')
                continue
            wdm_logger().debug(f'{driver_name} 尚未过期 {read_time}')
        return path_list

    def set_cache(self, driver_name, client_version, version, **kwargs):
        """
        写入缓存信息
        :param driver_name:
        :param client_version:
        :param version:
        :return:
        """
        self.__write_cache(
            driver_name=driver_name,
            client_version=client_version,
            version=version,
            **kwargs
        )

    def set_read_cache_data(self, driver_name, version):
        """
        写入当前读取 WebDriver 的时间
        :param driver_name:
        :param version:
        :return:
        """
        times = datetime.today()
        self.set_cache(
            driver_name=driver_name,
            version=version,
            last_read_time=f"{times}"  # 记录最后一次读取时间，并按照这个时间清理WebDriver
        )
        wdm_logger().debug(f'更新 {driver_name} - {version} 读取时间: {times}')

    def clear_cache_path(self, driver_name):
        """
        以当前时间为准，清除超过清理时间的 WebDriver 目录
        :param driver_name:
        :return:
        """
        path_list = self.get_cache_path_by_read_time(driver_name)
        cache_data = self.__read_cache

        for version in path_list:
            clear_path = os.path.join(self.root_dir, driver_name, version)
            if os.path.exists(clear_path):
                shutil.rmtree(clear_path)
            else:
                wdm_logger().warning(f'缓存目录无该路径: {clear_path}')
            cache_data[driver_name].pop(self.format_key(driver_name=driver_name, client_version=version))
            wdm_logger().info(f'清理过期WebDriver: {clear_path}')

        self.__dump_cache(cache_data)
