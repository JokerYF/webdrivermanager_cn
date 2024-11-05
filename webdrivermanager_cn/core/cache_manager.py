"""
Driver 缓存记录
"""
import json
import os
import shutil
import threading
import time

from webdrivermanager_cn.core.config import clear_wdm_cache_time
from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.os_manager import OSManager
from webdrivermanager_cn.core.time_ import get_time


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
    def __id(self):
        """
        返回当前对象ID
        :return:
        """
        return str(id(self))

    @property
    def thread_lock(self):
        """
        返回当前线程的ID
        :return:
        """
        return str(threading.current_thread().ident)

    @property
    def lock_file(self):
        """
        返回锁定文件path
        :return:
        """
        return os.path.join(self.__path, '.locked')

    @property
    def is_locked(self):
        """
        是否加锁
        :return:
        """
        return os.path.exists(self.lock_file)

    def lock(self):
        """
        加锁
        :return:
        """
        if not self.is_locked:
            with open(self.lock_file, 'w+') as f:
                f.write(f'{self.thread_lock}|{self.__id}')
            assert self.is_locked, '缓存加锁失败！'
            self.log.debug(f'缓存加锁成功！ {self.lock_file}')
        else:
            self.log.debug(f'缓存被其他线程加锁！{self.__get_lock_file_info}')

    def unlock(self):
        """
        解锁
        :return:
        """
        if self.is_locked:
            # 谁加锁谁解锁
            _thread, _key = self.__get_lock_file_info
            if _key == self.__id:
                os.remove(self.lock_file)
                assert not self.is_locked, '缓存解锁失败！'
                self.log.debug('缓存解锁成功！')
            else:
                self.log.debug(f'非当前线程和任务加锁！{_thread} | {_key}')

    def wait_unlock(self, timeout=30):
        """
        等待解锁
        :param timeout:
        :return:
        """
        start = time.time()
        while time.time() - start <= timeout:
            if not self.is_locked:
                return True

            _thread, _key = self.__get_lock_file_info
            if _thread == self.thread_lock:
                return True

            time.sleep(0.1)
        raise TimeoutError(f'等待缓存解锁超时！')

    @property
    def __get_lock_file_info(self):
        """
        读取解析文件
        :return:
        """
        if not self.is_locked:
            return None, None
        with open(self.lock_file, 'r+') as f:
            _thread = f.read()
        return _thread.split('|')[0], _thread.split('|')[1]


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
        # self.root_dir = os.path.join(self.__abs_path(root_dir), '.webdriver')
        # self.__json_path = os.path.join(self.root_dir, 'driver_cache.json')
        self.__lock = CacheLock(self.root_dir)
        self.__driver_name = None
        self.__driver_version = None
        self.__download_version = None

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
        self.__lock.wait_unlock()

        if not self.__json_exist:
            return {}
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if data else {}

    def __dump_cache(self, data: dict):
        """
        写入缓存
        :param data:
        :return:
        """
        with open(self.json_path, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def set_cache(self, **kwargs):
        """
        写入缓存文件
        :param kwargs:
        :return:
        """
        with self.__lock:
            data = self.__read_cache
            key = self.format_key

            if self.driver_name not in data.keys():
                data[self.driver_name] = {}
            if key not in data[self.driver_name].keys():
                data[self.driver_name][key] = {}

            driver_data = data[self.driver_name][key]
            driver_data.update(kwargs)
            try:
                driver_data.pop('driver_name')  # WebDriver cache 信息内不记录这些字段
            except KeyError:
                pass
            self.__dump_cache(data)

    @property
    def format_key(self) -> str:
        """
        格式化缓存 key 名称
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
        for version in self.get_clear_version_by_read_time:
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
            self.download_version = version
            cache_data[self.driver_name].pop(self.format_key)
            self.set_cache(**cache_data)

            self.log.info(f'清理过期WebDriver: {clear_path}')
