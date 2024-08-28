from webdrivermanager_cn.core.mirror_manager import MirrorType
from webdrivermanager_cn.driver.geckodriver import Geckodriver


class GeckodriverManager:
    def __init__(self, version='latest', path=None):
        self.__driver = Geckodriver(version=version, path=path)

    @property
    def driver(self):
        return self.__driver

    def set_ali_mirror(self):
        self.driver.mirror_type = MirrorType.Ali

    def set_huawei_mirror(self):
        self.driver.mirror_type = MirrorType.Huawei

    @property
    def get_cur_mirror(self):
        return self.driver.mirror_type

    def install(self) -> str:
        return self.driver.install()


class GeckodriverManagerAliMirror:
    def __init__(self, version='latest', path=None):
        self.manager = GeckodriverManager(version=version, path=path)
        self.manager.set_ali_mirror()

    def install(self) -> str:
        return self.manager.install()


class GeckodriverManagerHuaweiMirror:
    def __init__(self, version='latest', path=None):
        self.manager = GeckodriverManager(version=version, path=path)
        self.manager.set_huawei_mirror()

    def install(self) -> str:
        return self.manager.install()
