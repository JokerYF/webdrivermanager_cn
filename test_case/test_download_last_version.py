import os.path
import shutil

from webdrivermanager_cn import ChromeDriverManager, GeckodriverManager

base_path = os.getcwd()


class TestDownloadLastVersion:
    def test_download_chromedriver(self):
        # ali
        dm = ChromeDriverManager(path=base_path)
        dm.set_ali_mirror()
        path = dm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

        # huawei
        dm.set_huawei_mirror()
        path = dm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

    def test_download_geckodriver(self):
        # ali
        dm = GeckodriverManager(path=base_path)
        dm.set_ali_mirror()
        path = dm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

        # huawei
        dm.set_huawei_mirror()
        path = dm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))
