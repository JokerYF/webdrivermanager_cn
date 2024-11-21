import sys
from functools import wraps

import requests
from requests import session

from webdrivermanager_cn.core.config import verify_not, request_timeout
from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.version import VERSION


class Session(LogMixin):
    def __init__(self):
        self._s = session()
        self.__headers = {
            'User-Agent': f'python/{sys.version.split(" ")[0]} '
                          f'requests/{requests.__version__} '
                          f'webdrivermanager_cn/{VERSION}'
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, **kwargs):
        self.__headers.update(kwargs)

    def get(self, url):
        response = self._s.get(url, timeout=request_timeout(), verify=verify_not(), headers=self.headers)
        self.log.debug(f"GET {url} - {response.status_code} - headers: {self.headers}")
        response.raise_for_status()
        return response

    def close(self):
        self._s.close()


CACHE = {}


def url_cache(func):
    global CACHE
    log = LogMixin().log

    @wraps(func)
    def wrapper(url):
        if url not in CACHE.keys():
            log.debug(f"未命中请求缓存 {url}")
            res = func(url)
            CACHE[url] = res
            log.debug(f"请求缓存已添加 {url}")
        log.debug(f"命中请求缓存 {url}")
        return CACHE[url]

    return wrapper


@url_cache
def request_get(url):
    with Session() as r:
        return r.get(url)
