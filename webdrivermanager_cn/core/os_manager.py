"""
获取操作系统相关信息
"""

import platform
import sys


class OSType:
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


class OSManager:
    """
    获取操作系统相关信息
    """

    def __init__(self, os_type=None):
        self._os_type = os_type

    @property
    def get_os_name(self):
        """
        获取操作系统名称
        :return:
        """
        pl = sys.platform
        if pl in ['linux', 'linux2']:
            return OSType.LINUX
        elif pl == "darwin":
            return OSType.MAC
        elif pl in ['win32', 'cygwin']:
            return OSType.WIN
        raise OSError(f'WDM未适配当前OS系统: {pl}')

    @property
    def get_os_architecture(self):
        """
        获取操作系统位数
        :return:
        """
        if platform.machine().endswith("64"):
            return 64
        else:
            return 32

    @property
    def get_os_type(self):
        """
        获取操作系统类型
        :return:
        """
        if self._os_type:
            return self._os_type
        return f"{self.get_os_name}{self.get_os_architecture}"

    @staticmethod
    def is_arch(os_sys_type):
        """
        判断是否为mac M系列芯片
        :param os_sys_type:
        :return:
        """
        if "_m1" in os_sys_type or "_m2" in os_sys_type:
            return True
        return platform.processor() != "i386"

    @property
    def get_mac_framework(self):
        """
        获取mac操作系统芯片类型
        :return:
        """
        machine_type = platform.machine()
        if machine_type == "arm64":
            return "_m1"
        elif machine_type == "aarch64":
            return "_m2"

    @property
    def is_aarch64(self):
        return platform.machine() == 'aarch64'

    @property
    def get_framework(self):
        """
        获取操作系统架构
        :return:
        """
        if self.is_mac:
            return self.get_mac_framework
        return ''

    @property
    def is_win(self):
        return self.get_os_name == OSType.WIN

    @property
    def is_linux(self):
        return self.get_os_name == OSType.LINUX

    @property
    def is_mac(self):
        return self.get_os_name == OSType.MAC
