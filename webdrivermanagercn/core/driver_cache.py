import json
import os

from webdrivermanagercn.core.os_manager import OSManager


class DriverCacheManager:
    def __init__(self, root_dir=None):
        if not root_dir:
            root_dir = os.path.expanduser('~')
        self.root_dir = os.path.join(root_dir, '.webdriver')
        self.__json_path = os.path.join(self.root_dir, 'driver_cache.json')

    @property
    def __json_exist(self):
        return os.path.exists(self.__json_path)

    def __read_cache(self) -> dict:
        if not self.__json_exist:
            return {}
        with open(self.__json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __write_cache(self, **kwargs):
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
    def format_key(driver_name, version):
        return f'{driver_name}_{OSManager().get_os_name}_{version}'

    def get_cache(self, driver_name, version):
        if not self.__json_exist:
            return None
        try:
            return self.__read_cache()[driver_name][self.format_key(driver_name, version)]['path']
        except KeyError:
            return None

    def set_cache(self, driver_name, version, update, path):
        self.__write_cache(
            driver_name=driver_name,
            version=version,
            update=update,
            path=path
        )
