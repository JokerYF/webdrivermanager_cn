from webdrivermanager_cn.drivers.geckodriver import Geckodriver


class GeckodriverManager:
    def __init__(self, version=None, path=None):
        self.geckodriver = Geckodriver(version=version, path=path)

    def install(self) -> str:
        """
        安装 geckodriver，返回Driver绝对路径
        :return:
        """
        return self.geckodriver.install()
