"""
获取操作系统相关信息
"""

import platform
import re
import subprocess
import sys


class OSType:
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


class ClientType:
    Chrome = "google-chrome"
    Chromium = "chromium"
    Edge = "edge"
    Firefox = "firefox"
    Safari = "safari"


CLIENT_PATTERN = {
    ClientType.Chrome: r"\d+\.\d+\.\d+.\d+",
}


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
        if pl == "linux" or pl == "linux2":
            return OSType.LINUX
        elif pl == "darwin":
            return OSType.MAC
        elif pl == "win32" or pl == "cygwin":
            return OSType.WIN

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
        if "_m1" in os_sys_type:
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
        else:
            return None

    @property
    def get_framework(self):
        """
        获取操作系统架构
        :return:
        """
        if self.get_os_name == OSType.MAC:
            return self.get_mac_framework
        elif self.get_os_name == OSType.LINUX:
            ...
        return None


class GetVersion:
    @staticmethod
    def cmd_dict(client):
        os_type = OSManager().get_os_name
        cmd_map = {
            OSType.MAC: {
                ClientType.Chrome: "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
            },
            OSType.WIN: {},
            OSType.LINUX: {},
        }
        return cmd_map[os_type][client], CLIENT_PATTERN[client]

    def get_version(self, client):
        return self.read_version_from_cmd(*self.cmd_dict(client))

    @staticmethod
    def read_version_from_cmd(cmd, pattern):
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                shell=True,
        ) as stream:
            stdout = stream.communicate()[0].decode()
            version = re.search(pattern, stdout)
            version = version.group(0) if version else None
        return version


if __name__ == "__main__":
    # print(RunCmd().get_version(ClientType.Chrome))
    print(OSManager().get_os_info())
