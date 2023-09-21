from webdrivermanagercn.drivers.chrome import ChromeDriver


class ChromeDriverManager(ChromeDriver):
    def __init__(self, version=None, path=None):
        super().__init__(version=version, path=path)

    def install(self):
        return super().install()


if __name__ == '__main__':
    print(ChromeDriverManager(version='85.0.4183.83').install())
