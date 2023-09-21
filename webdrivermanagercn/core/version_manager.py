"""
搜索版本，如果版本不存在，则找大一或者小一版本
"""
import re
import subprocess

import requests
from packaging import version as vs

from webdrivermanagercn.core import config
from webdrivermanagercn.core.os_manager import OSManager, OSType


class ClientType:
    Chrome = "google-chrome"
    Chromium = "chromium"
    Edge = "edge"
    Firefox = "firefox"
    Safari = "safari"


CLIENT_PATTERN = {
    ClientType.Chrome: r"\d+\.\d+\.\d+.\d+",
}


class GetUrl:
    """
    根据版本获取url
    """

    def __init__(self):
        self._version = ''

    @property
    def _version_obj(self):
        return vs.parse(self._version)

    @property
    def get_host(self):
        if self._version_obj.major >= 115:
            return config.ChromeDriverUrlNew
        else:
            return config.ChromeDriverUrl

    @property
    def _version_list(self):
        return [i['name'].replace('/', '') for i in requests.get(self.get_host).json()]

    def get_correct_version(self):
        _version = self._version
        return self.__compare_versions(_version, self._version_list)

    @staticmethod
    def __compare_versions(target_version, version_list):
        """
        根据目标version检查并获取版本
        如果当前版本在版本列表中，则直接返回列表，否则返回当前版本小的一个版本
        :param target_version:
        :param version_list:
        :return: version
        """
        if target_version not in version_list:
            lesser_version = None
            for version in version_list:
                if version < target_version:
                    lesser_version = version
                else:
                    break
            return lesser_version
        return target_version


class GetClientVersion(GetUrl):
    """
    获取当前环境下浏览器版本
    """

    @staticmethod
    def cmd_dict(client):
        os_type = OSManager().get_os_name
        cmd_map = {
            OSType.MAC: {
                ClientType.Chrome: "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
            },
            OSType.WIN: {
                ClientType.Chrome: 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            },
            OSType.LINUX: {},
        }
        return cmd_map[os_type][client], CLIENT_PATTERN[client]

    @staticmethod
    def __read_version_from_cmd(cmd, pattern):
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

    def get_version(self, client):
        self._version = self.__read_version_from_cmd(*self.cmd_dict(client))
        return self.get_correct_version()
