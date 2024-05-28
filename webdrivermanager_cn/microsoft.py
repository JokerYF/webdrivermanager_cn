from webdrivermanager_cn.drivers.microsoft import EdgeDriver


class EdgeWebDriverManager:
    def __init__(self, version='latest', path=None):
        self.__driver = EdgeDriver(
            version=version,
            path=path,
        )

    def install(self):
        return self.__driver.install()
