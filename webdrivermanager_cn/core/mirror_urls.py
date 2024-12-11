class VersionApi:
    ChromeDriverApiNew = 'https://cdn.npmmirror.com/binaries/chrome-for-testing/last-known-good-versions.json'
    ChromeDriverLastPastVersion = 'https://cdn.npmmirror.com/binaries/chrome-for-testing/latest-patch-versions-per-build.json'
    GeckodriverApiNew = 'https://gitee.com/Joker_JH/DriverRelease/raw/master/GeckodriverLastVersion.json'


class PublicMirror:
    EdgeDriverUrl = 'https://msedgedriver.azureedge.net'
    ChromeDriver = 'https://googlechromelabs.github.io/chrome-for-testing'
    GeckodriverApi = 'https://api.github.com/repos/mozilla/geckodriver/releases'


class AliMirror:
    ChromeDriverUrl = 'https://registry.npmmirror.com/-/binary/chromedriver'
    ChromeDriverUrlNew = 'https://registry.npmmirror.com/-/binary/chrome-for-testing'
    GeckodriverUrl = 'https://registry.npmmirror.com/-/binary/geckodriver'
    EdgeDriverUrl = 'https://registry.npmmirror.com/-/binary/edgedriver'


class HuaweiMirror:
    ChromeDriverUrl = 'https://mirrors.huaweicloud.com/chromedriver'
    ChromeDriverVersion = 'https://mirrors.huaweicloud.com/chromedriver/.index.json'
    GeckodriverUrl = 'https://mirrors.huaweicloud.com/geckodriver'
    GeckodriverVersion = 'https://mirrors.huaweicloud.com/geckodriver/.index.json'
