from webdrivermanager_cn.core.log_manager import LogMixin
from webdrivermanager_cn.core.mirror_urls import AliMirror, HuaweiMirror, PublicMirror, VersionApi


class MirrorType:
    Ali = 'npmmirror'
    Huawei = 'huaweicloud'


class MirrorManager(LogMixin):
    def __init__(self, mirror_type: MirrorType = None):
        self.__type = mirror_type

    def mirror_type(self):
        if self.__type is None:
            self.__type = MirrorType.Ali

        if not isinstance(self.__type, MirrorType):
            raise TypeError(f'mirror_type 参数传参类型错误，应为 MirrorType, 实际 {type(self.__type)}')
        self.log.debug(f'mirror_type: {self.__type}')
        return self.__type

    @property
    def is_ali(self):
        return self.mirror_type() == MirrorType.Ali

    @property
    def is_huawei(self):
        return self.mirror_type() == MirrorType.Huawei


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
