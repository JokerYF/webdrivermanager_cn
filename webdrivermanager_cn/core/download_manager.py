"""
下载
"""
import os

import requests as requests

from webdrivermanager_cn.core.log_manager import wdm_logger


class DownloadManager:
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
        wdm_logger().debug(f'开始执行下载: {url}')
        response = requests.get(url)
        wdm_logger().debug(f'url: {url} - {response.status_code}')
        response.raise_for_status()
        wdm_logger().debug(f'本地下载路径: {down_path}')
        os.makedirs(down_path, exist_ok=True)
        file_path = os.path.join(down_path, self.get_filename_by_url(url))
        with open(file_path, "wb") as f:
            f.write(response.content)
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
