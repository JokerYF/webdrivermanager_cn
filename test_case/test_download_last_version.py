import os.path
import shutil

from webdrivermanager_cn import ChromeDriverManager, GeckodriverManager

base_path = os.getcwd()


class TestDownloadLastVersion:
    cm = ChromeDriverManager(path=base_path)
    gm = GeckodriverManager(path=base_path)

    @staticmethod
    def teardown_method():
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

    def test_download_chromedriver_by_ali(self):
        # ali
        self.cm.set_ali_mirror()
        path = self.cm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'

    def test_download_chromedriver_by_huawei(self):
        # huawei
        self.cm.set_huawei_mirror()
        path = self.cm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'

    def test_download_geckodriver_by_ali(self):
        # ali
        self.gm.set_ali_mirror()
        path = self.gm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'

    def test_download_geckodriver_by_huawei(self):
        # huawei
        self.gm.set_huawei_mirror()
        path = self.gm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'
