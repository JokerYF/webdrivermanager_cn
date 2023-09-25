"""
下载
"""
import os

import requests as requests


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
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(down_path, exist_ok=True)
        file_path = os.path.join(down_path, self.get_filename_by_url(url))
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path

    @staticmethod
    def get_filename_by_url(url):
        """
        根据url提取压缩文件名
        :param url:
        :return:
        """
        url_paser = url.split('/')
        return url_paser[-1]
