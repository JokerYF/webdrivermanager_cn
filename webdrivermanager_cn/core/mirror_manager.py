from abc import ABC, abstractmethod

from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.mirror_urls import AliMirror, HuaweiMirror, PublicMirror, VersionApi


class MirrorType:
    Ali = 'npmmirror.com'
    Huawei = 'huaweicloud.com'


class MirrorManager(ABC, LogMixin):
    def __init__(self, mirror_type: MirrorType = None):
        self.__type = mirror_type

    @property
    def mirror_type(self):
        if self.__type is None:
            self.__type = MirrorType.Ali
        assert self.__type in [MirrorType.Ali, MirrorType.Huawei], '传入的源类型不正确！'
        return self.__type

    @property
    def is_ali(self):
        return self.mirror_type == MirrorType.Ali

    @property
    def is_huawei(self):
        return self.mirror_type == MirrorType.Huawei

    @abstractmethod
    def mirror_url(self, *args, **kwargs):
        pass

    @abstractmethod
    def latest_version_url(self, *args, **kwargs):
        pass

    def latest_patch_version_url(self, *args, **kwargs):
        pass


class ChromeDriverMirror(MirrorManager):
    def mirror_url(self, version):
        if self.is_ali:
            from webdrivermanager_cn.core.version_manager import ChromeDriverVersionManager
            if ChromeDriverVersionManager(version).is_new_version:
                return AliMirror.ChromeDriverUrlNew
            return AliMirror.ChromeDriverUrl
        elif self.is_huawei:
            return HuaweiMirror.ChromeDriverUrl

    @property
    def latest_version_url(self):
        return VersionApi.ChromeDriverApiNew

    @property
    def latest_patch_version_url(self):
        return VersionApi.ChromeDriverLastPatchVersion


class GeckodriverMirror(MirrorManager):
    def mirror_url(self):
        if self.is_ali:
            return AliMirror.GeckodriverUrl
        elif self.is_huawei:
            return HuaweiMirror.GeckodriverUrl

    @property
    def latest_version_url(self):
        return VersionApi.GeckodriverApiNew


class EdgeDriverMirror(MirrorManager):
    def mirror_url(self):
        if self.is_ali:
            return AliMirror.EdgeDriverUrl
        else:
            return PublicMirror.EdgeDriverUrl

    @property
    def latest_version_url(self):
        return f'{PublicMirror.EdgeDriverUrl}/LATEST_STABLE'
