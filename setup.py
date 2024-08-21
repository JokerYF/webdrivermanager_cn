import setuptools

from webdrivermanager_cn_bak.version import VERSION

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="webdrivermanager_cn",
    python_requires=">=3.7",
    long_description=readme,
    long_description_content_type="text/markdown",
    version=VERSION,
    author="御风",
    author_email="eternallyyf@163.com",
    url="https://gitee.com/Joker_JH/webdrivermanagercn",
    packages=setuptools.find_packages(include=["webdrivermanager_cn*"]),
    install_requires=["requests", "packaging"],
    license="Apache License 2.0",
    description="基于阿里源开发的WebDriver管理工具",
)
