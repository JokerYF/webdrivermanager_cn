import os

from webdrivermanager_cn.core.log_manager import LogMixin


class EnvMixin(LogMixin):
    """
    环境变量混入类
    用于执行代码时读写环境变量，代码执行结束后释放写入的环境变量
    """

    @staticmethod
    def get(key, default=None):
        """
        获取环境变量
        :param key: 环境变量名
        :param default: 默认值
        :return:
        """
        value = os.getenv(key, default)
        return value

    def set(self, key, value):
        """
        设置环境变量
        :param key: 环境变量名
        :param value: 环境变量值
        :return:
        """
        os.environ[key] = str(value)
        self.log.debug(f"set env {key} - {value}")
