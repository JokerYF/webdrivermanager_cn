from webdrivermanager_cn.drivers.microsoft import EdgeDriverManager


class EdgeWebDriverManager:
    def __init__(self, version=None, path=None):
        self.__driver = EdgeDriverManager(
            version=version,
            path=path,
        )

    def install(self):
        return self.__driver.install()
