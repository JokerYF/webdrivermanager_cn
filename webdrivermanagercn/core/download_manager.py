import os

import requests as requests


class DownloadManager:
    def download_file(self, url, down_path):
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(down_path, exist_ok=True)
        file_path = os.path.join(down_path, self.get_filename_by_url(url))
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path

    @staticmethod
    def get_filename_by_url(url):
        url_paser = url.split('/')
        return url_paser[-1]
