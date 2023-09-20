import os

from drivers.chrome import ChromeDriver


class ChromeDriverManager(ChromeDriver):
    def __init__(self, version=None, root_dir=None):
        super().__init__(version=version, root_dir=root_dir)

    def install(self):
        return super().install()


if __name__ == '__main__':
    print(ChromeDriverManager('113.0.5672.63', os.getcwd()).install())
