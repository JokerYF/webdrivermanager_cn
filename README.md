<div align="center">

# WebDriverManager CN

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/webdrivermanager-cn.svg)](https://pypi.org/project/webdrivermanager-cn/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/eternallyyf/webdrivermanagercn/blob/master/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/webdrivermanager-cn.svg)](https://pypi.org/project/webdrivermanager-cn/)

**基于国内镜像源的 WebDriver 自动管理工具**

[简体中文](README.md)

</div>

---

## 📖 简介

WebDriverManager CN 是一个基于 [阿里云镜像源](https://www.npmmirror.com/)
和 [华为云镜像源](https://mirrors.huaweicloud.com/) 的 WebDriver 自动下载管理工具，是 `webdriver_manager` 的国内镜像版本。

### ✨ 特性

- 🚀 **自动下载** - 自动匹配浏览器版本并下载对应的 WebDriver
- 🇨🇳 **国内加速** - 支持阿里云、华为云镜像源，下载速度快
- 💾 **智能缓存** - 自动缓存已下载的驱动，避免重复下载
- 🧹 **自动清理** - 可配置自动清理过期的驱动文件
- 🔄 **灵活切换** - 支持多镜像源切换，保证可用性
- 🎯 **跨平台** - 支持 Windows、MacOS、Linux

---

## 📦 安装

### 使用 pip 安装

```bash
pip install webdrivermanager_cn
```

### 升级到最新版本

```bash
pip install -U webdrivermanager_cn
```

---

## 🚀 快速开始

### ChromeDriver 使用示例

#### 方式一：使用阿里云镜像源（推荐）

```python
from webdrivermanager_cn import ChromeDriverManagerAliMirror

driver_path = ChromeDriverManagerAliMirror().install()
```

#### 方式二：使用华为云镜像源

```python
from webdrivermanager_cn import ChromeDriverManagerHuaweiMirror

driver_path = ChromeDriverManagerHuaweiMirror().install()
```

#### 方式三：手动切换镜像源

```python
from webdrivermanager_cn import ChromeDriverManager

driver = ChromeDriverManager()
driver.set_ali_mirror()  # 切换为阿里源（默认）
# driver.set_huawei_mirror() # 切换为华为源

driver_path = driver.install()
```

### Geckodriver (Firefox) 使用示例

#### 使用阿里云镜像源

```python
from webdrivermanager_cn import GeckodriverManagerAliMirror

driver_path = GeckodriverManagerAliMirror().install()
```

#### 使用华为云镜像源

```python
from webdrivermanager_cn import GeckodriverManagerHuaweiMirror

driver_path = GeckodriverManagerHuaweiMirror().install()
```

#### 手动切换镜像源

```python
from webdrivermanager_cn import GeckodriverManager

driver = GeckodriverManager()
driver.set_ali_mirror()  # 切换为阿里源（默认）
# driver.set_huawei_mirror() # 切换为华为源

driver_path = driver.install()
```

---

## 🛠️ 配置选项

### 日志配置

```python
import os
import logging

# 开启日志功能（默认关闭）
os.environ['WDM_LOG'] = 'true'

# 设置日志级别（默认为 INFO）
os.environ['WDM_LOG_LEVEL'] = str(logging.INFO)
```

### 自定义 Logger

```python
from webdrivermanager_cn.core.log_manager import set_logger
import logging

# 使用自定义 logger
my_logger = logging.getLogger('my_custom_logger')
set_logger(my_logger)
```

### 缓存管理

```python
import os

# 设置缓存清理时间（单位：天，默认为 5 天）
# 会自动删除 5 天前下载的旧版本 WebDriver
os.environ['WDM_CACHE_TIME'] = '5'
```

---

## 📊 支持的浏览器

|   浏览器   | Windows | MacOS | Linux |
|:-------:|:-------:|:-----:|:-----:|
| Chrome  |    ✅    |   ✅   |   ✅   |
| Firefox |    ✅    |   ✅   |   ✅   |

> 💡 如需支持其他浏览器，欢迎提交 [Issue](https://gitee.com/Joker_JH/webdrivermanagercn/issues)

---

## 🤝 贡献

欢迎贡献代码、提出建议或报告问题！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

如果您发现了新的国内镜像源，欢迎提交 Issue 或 PR！

---

## 📄 许可证

本项目基于 [Apache-2.0](LICENSE) 协议开源。

---

## ⚠️ 免责声明

本项目仅供自动化测试工具使用，请勿用于非法用途。对于任何使用者的行为，本项目及作者不承担任何责任。

本项目依赖以下第三方服务，如有相关问题，会积极推进解决，但无法保证完全解决：

- [Gitee](https://gitee.com/)
- [阿里云开源镜像站](https://www.npmmirror.com/)
- [华为云开源镜像站](https://mirrors.huaweicloud.com/home)

---

## 📮 联系方式

- **作者**: 御风
- **Email**: eternallyyf@163.com
- **项目地址**: [Gitee](https://gitee.com/Joker_JH/webdrivermanagercn)

如果在使用过程中遇到任何问题，欢迎提交 [Issue](https://gitee.com/Joker_JH/webdrivermanagercn/issues)！

---

## 💡 开发背景

作者是一名测试开发工程师，在自动化测试工作中使用 `webdriver_manager` 解决了 Chrome 频繁更新导致 ChromeDriver 无法使用的问题。

然而，2023年中期，ChromeDriver 官方修改了发布方式，导致国内大部分镜像源无法正确同步新版本（停留在 114
版本）。虽然阿里云镜像已经完成了新版同步，但原有的下载方式已经无法适配。

因此，作者研究源码后决定重新开发一个基于国内镜像源的 WebDriver 管理工具，帮助无法访问 GitHub 的团队和个人继续使用自动化测试。

---

<div align="center">

**如果这个项目对您有帮助，请给一个 ⭐️ Star！**

</div>
