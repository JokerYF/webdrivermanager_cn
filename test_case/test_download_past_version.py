import logging
import os.path
import shutil

from webdrivermanager_cn import ChromeDriverManager, GeckodriverManager

base_path = os.getcwd()

os.environ['WDM_LOG'] = 'true'
os.environ['WDM_LOG_LEVEL'] = f'{logging.DEBUG}'


class TestDownloadPastVersion:
    def test_download_chromedriver_past_version(self):
        version = '95.0.4638.10'
        # ali
        dm = ChromeDriverManager(path=base_path, version=version)
        dm.set_ali_mirror()
        path = dm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

        # 华为源下载115以下版本有问题，暂时不做测试
        # huawei
        # dm.set_huawei_mirror()
        # path = dm.install()
        # assert os.path.exists(path), 'ChromeDriver下载失败'
        # shutil.rmtree(os.path.join(base_path, '.webdriver'))

    def test_download_chromedriver_past_version2(self):
        version = '115.0.5781.0'
        # ali
        dm = ChromeDriverManager(path=base_path, version=version)
        dm.set_ali_mirror()
        path = dm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

        # huawei
        dm.set_huawei_mirror()
        path = dm.install()
        assert os.path.exists(path), 'ChromeDriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

    def test_download_geckodriver_past_version(self):
        version = 'v0.10.0'
        # ali
        dm = GeckodriverManager(path=base_path, version=version)
        dm.set_ali_mirror()
        path = dm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))

        # huawei
        dm.set_huawei_mirror()
        path = dm.install()
        assert os.path.exists(path), 'Geckodriver下载失败'
        shutil.rmtree(os.path.join(base_path, '.webdriver'))
