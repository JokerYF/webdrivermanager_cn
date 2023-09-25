from webdrivermanager_cn.drivers.geckodriver import Geckodriver


class GeckodriverManager(Geckodriver):
    def __init__(self, version=None, path=None):
        super().__init__(version=version, path=path)

    def install(self) -> str:
        return super().install()
