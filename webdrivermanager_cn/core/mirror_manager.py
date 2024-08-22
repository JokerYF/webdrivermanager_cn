from webdrivermanager_cn.core.mirror_urls import AliMirror, HuaweiMirror, PublicMirror


class MirrorType:
    Ali = 'npmmirror'
    Huawei = 'huaweicloud'


class MirrorManager:
    def __init__(self, mirror_type: MirrorType = None):
        self.__type = mirror_type

    def mirror_type(self):
        if self.__type is None:
            self.__type = MirrorType.Ali

        if not isinstance(self.__type, MirrorType):
            raise TypeError(f'mirror_type 参数传参类型错误，应为 MirrorType, 实际 {type(self.__type)}')

        return self.__type

    @property
    def is_ali(self):
        return self.mirror_type() == MirrorType.Ali

    @property
    def is_huawei(self):
        return self.mirror_type() == MirrorType.Huawei

    def chrome_driver_mirror(self, version):
        if self.is_ali:
            from webdrivermanager_cn.core.version_manager import ChromeDriverVersionManager
            if ChromeDriverVersionManager(version).is_new_version:
                return AliMirror.ChromeDriverUrlNew
            return AliMirror.ChromeDriverUrl
        elif self.is_huawei:
            return HuaweiMirror.ChromeDriverUrl

    def geckodriver_mirror(self):
        if self.is_ali:
            return AliMirror.GeckodriverUrl
        elif self.is_huawei:
            return HuaweiMirror.GeckodriverUrl

    def edge_driver_mirror(self):
        if self.is_ali:
            return AliMirror.EdgeDriverUrl
        else:
            return PublicMirror.EdgeDriverUrl
