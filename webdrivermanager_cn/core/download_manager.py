"""
下载
"""
import os

import requests as requests
import urllib3

from webdrivermanager_cn.core.config import verify_not, request_timeout
from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.version import VERSION


def headers(**kwargs):
    _headers = {
        'User-Agent': f'python-requests/{requests.__version__} webdrivermanagercn/{VERSION}'
    }
    _headers.update(kwargs)
    return _headers


class DownloadManager(LogMixin):
    """
    文件下载
    """

    def download_file(self, url, down_path):
        """
        从指定的url中下载文件到指定目录中
        :param url:
        :param down_path:
        :return:
        """
        self.log.debug(f'开始执行下载: {url}')
        response = requests.get(url, timeout=request_timeout(), headers=headers(), verify=verify_not())
        self.log.debug(f'url: {url} - {response.status_code}')
        response.raise_for_status()
        response.close()
        self.log.debug(f'本地下载路径: {down_path}')
        os.makedirs(down_path, exist_ok=True)
        file_path = os.path.join(down_path, self.get_filename_by_url(url))
        self.__load_file(url, file_path)
        return file_path

    @staticmethod
    def get_filename_by_url(url):
        """
        根据url提取压缩文件名
        :param url:
        :return:
        """
        url_parser = url.split("/")
        return url_parser[-1]

    @staticmethod
    def __load_file(url, down_path):
        """
        从指定的url中下载文件到指定目录中
        :param url:
        :param down_path:
        :return:
        """
        http = urllib3.PoolManager()
        response = http.request('GET', url, preload_content=False)

        with open(down_path, 'wb') as out_file:
            while True:
                data = response.read(4096)  # 每次读取的块大小，可根据需要调整
                if not data:
                    break
                out_file.write(data)

        response.release_conn()
