from webdrivermanagercn.drivers.chrome import ChromeDriver


class ChromeDriverManager(ChromeDriver):
    def __init__(self, version=None, root_dir=None):
        super().__init__(version=version, root_dir=root_dir)

    def install(self):
        return super().install()
