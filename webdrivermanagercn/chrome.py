from webdrivermanagercn.drivers.chrome import ChromeDriver


class ChromeDriverManager(ChromeDriver):
    def __init__(self, version=None, path=None):
        super().__init__(version=version, path=path)

    def install(self):
        return super().install()
