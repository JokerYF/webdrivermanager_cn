"""
Driver 缓存记录
"""
import json
import os
import shutil
import time

from webdrivermanager_cn_bak.core.config import clear_wdm_cache_time
from webdrivermanager_cn_bak.core.log_manager import LogMixin
from webdrivermanager_cn_bak.core.os_manager import OSManager
from webdrivermanager_cn_bak.core.time_ import get_time


class CacheLock(LogMixin):
    """
    实现缓存加锁
    """

    def __init__(self, cache_path):
        self.__path = cache_path

    def __enter__(self):
        self.lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()

    @property
    def lock_file(self):
        return os.path.join(self.__path, '.locked')

    @property
    def is_locked(self):
        return os.path.exists(self.lock_file)

    def lock(self):
        if not self.is_locked:
            open(self.lock_file, 'w').close()
            assert self.is_locked, '缓存加锁失败！'
        self.log.debug('缓存加锁成功！')

    def unlock(self):
        if self.is_locked:
            os.remove(self.lock_file)
            assert not self.is_locked, '缓存解锁失败！'
        self.log.debug('缓存解锁成功！')

    def wait_unlock(self, timeout=30):
        start = time.time()
        while time.time() - start <= timeout:
            if not self.is_locked:
                return True
            time.sleep(0.1)
        raise TimeoutError(f'等待缓存解锁超时！')


class DriverCacheManager(LogMixin):
    """
    Driver 缓存管理
    """

    def __init__(self, root_dir=None):
        """
        缓存管理
        :param root_dir:
        """
        self.root_dir = os.path.join(self.__abs_path(root_dir), '.webdriver')
        self.__json_path = os.path.join(self.root_dir, 'driver_cache.json')
        self.__lock = CacheLock(self.root_dir)
        self.__driver_name = None
        self.__driver_version = None
        self.__download_version = None

    @staticmethod
    def __abs_path(path):
        if not path:
            path = os.path.expanduser('~')
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        return path

    @property
    def driver_version(self):
        if not self.driver_version:
            raise ValueError
        return self.__driver_version

    @driver_version.setter
    def driver_version(self, value):
        self.__driver_version = value

    @property
    def driver_name(self):
        if not self.__driver_name:
            raise ValueError
        return self.__driver_name

    @driver_name.setter
    def driver_name(self, value):
        self.__driver_name = value

    @property
    def download_version(self):
        if not self.__download_version:
            raise ValueError
        return self.__download_version

    @download_version.setter
    def download_version(self, value):
        self.__download_version = value

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
        self.__lock.wait_unlock()

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
        with self.__lock:
            data = self.__read_cache
            key = self.format_key

            if self.driver_version not in data.keys():
                data[self.driver_name] = {}
            if key not in data[self.driver_name].keys():
                data[self.driver_name][key] = {}

            driver_data = data[self.driver_name][key]
            driver_data.update(kwargs)
            driver_data.pop('driver_name')  # WebDriver cache 信息内不记录这些字段
            self.__dump_cache(data)

    @property
    def format_key(self) -> str:
        """
        格式化缓存 key 名称
        :param driver_name:
        :param version:
        :return:
        """
        return f'{self.driver_name}_{OSManager().get_os_name}_{self.download_version}'

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
            return self.__read_cache[self.driver_name][self.format_key][key]
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
        for driver, info in self.__read_cache[self.driver_name].items():
            _version = info['version']
            try:
                read_time = int(info['last_read_time'])
            except (KeyError, ValueError):
                read_time = 0
            if not read_time or int(get_time('%Y%m%d')) - read_time >= time_interval:
                _clear_version.append(_version)
                self.log.debug(f'{self.driver_name} - {_version} 已过期 {read_time}, 即将清理!')
                continue
            self.log.debug(f'{self.driver_name} - {_version} 尚未过期 {read_time}')
        return _clear_version

    def set_cache(self, driver_name, version, **kwargs):
        """
        写入缓存信息
        :param driver_name:
        :param version:
        :return:
        """
        self.__write_cache(
            driver_name=driver_name,
            version=version,
            **kwargs
        )

    def set_read_cache_date(self):
        """
        写入当前读取 WebDriver 的时间
        :return:
        """
        times = get_time('%Y%m%d')
        if self.get_cache(key='last_read_time') != times:
            self.set_cache(driver_name=self.driver_name, version=self.download_version, last_read_time=f"{times}")
            self.log.debug(f'更新 {self.driver_name} - {self.download_version} 读取时间: {times}')

    def clear_cache_path(self):
        """
        以当前时间为准，清除超过清理时间的 WebDriver 目录
        :return:
        """
        _clear_version = self.get_clear_version_by_read_time

        for version in _clear_version:
            clear_path = os.path.join(self.root_dir, self.driver_name, version)
            if os.path.exists(clear_path):
                try:
                    shutil.rmtree(clear_path)
                except Exception as e:
                    self.log.error(f'清理过期WebDriver: {clear_path} 失败! {e}')
                    continue
            else:
                self.log.warning(f'缓存目录无该路径: {clear_path}')

            cache_data = self.__read_cache
            cache_data[self.driver_name].pop(self.format_key)
            self.__dump_cache(cache_data)

            self.log.info(f'清理过期WebDriver: {clear_path}')
