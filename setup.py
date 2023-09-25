import setuptools

setuptools.setup(
    name='webdrivermanager_cn',
    python_requires='>=3.7',
    version='0.2.1',
    author_email='eternallyyf@163.com',
    url="https://gitee.com/Joker_JH/webdrivermanagercn",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'packaging'
    ],
)
