import os

import requests as requests

from webdrivermanagercn.core.config import wdm_logger as log


class DownloadManager:
    def download_file(self, url, down_path):
        log.info(f'driver 下载 url: {url}')
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(down_path, exist_ok=True)
        file_path = os.path.join(down_path, self.get_filename_by_url(url))
        with open(file_path, 'wb') as f:
            f.write(response.content)
        log.info(f'driver 下载完成: {file_path}')
        return file_path

    @staticmethod
    def get_filename_by_url(url):
        url_paser = url.split('/')
        return url_paser[-1]


if __name__ == '__main__':
    a = DownloadManager().download_file(
        'https://registry.npmmirror.com/-/binary/chromedriver/114.0.5735.16/chromedriver_mac64.zip',
        os.getcwd())
    print(a)
