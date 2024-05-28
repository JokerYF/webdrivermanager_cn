import sys

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

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, **kwargs):
        for k, v in kwargs:
            self.__headers[k] = v

    def get(self, url):
        self.log.debug(f"GET {url} - {self.__headers}")
        response = self._s.get(url, timeout=request_timeout(), verify=verify_not())
        self.log.debug(f"GET {url} - {response.status_code}")
        response.raise_for_status()
        return response

    def close(self):
        self._s.close()


class Request:
    def __init__(self):
        self.__session = Session()

    def __enter__(self):
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()
        return self


def request_get(url):
    with Request() as r:
        return r.get(url)
