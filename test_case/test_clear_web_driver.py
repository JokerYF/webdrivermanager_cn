import os.path
import shutil

from webdrivermanager_cn import ChromeDriverManager
from webdrivermanager_cn.core.cache_manager import DriverCacheManager
from webdrivermanager_cn.core.driver import DriverType


class TestClearWebDriver:
    version = '115.0.5781.0'
    path = os.getcwd()

    def teardown_method(self):
        shutil.rmtree(os.path.join(self.path, '.webdriver'))

    def test_clear_web_driver(self):
        cm = ChromeDriverManager(path=self.path, version=self.version)
        path = cm.install()
        assert os.path.exists(path), 'WebDriver下载失败'

        cache_manager = DriverCacheManager(root_dir=self.path)
        cache_manager.driver_name = DriverType.chrome
        cache_manager.download_version = self.version

        cache_manager.set_cache(last_read_time="20200101")

        cache_manager.clear_cache_path()

        assert not os.path.exists(path), 'WebDriver清理失败'
        assert not cache_manager.get_cache('path'), 'WebDriverCache清理失败'
