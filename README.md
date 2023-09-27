# WerDriverManagerCn

> 基于[阿里源](https://www.npmmirror.com/)
> 开发，灵感来源：[webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)，向原作者致敬！

## 开发背景

作者是测开一枚，一直在公司默默无闻的做着自动化测试，偶然公司同事安利`webdriver_manager`
这个模块可以有效解决Chrome频繁更新导致ChromeDriver无法使用的问题，可以直接更换国内源，解决默认为github源而导致下载慢或者失败的问题。

自动化项目引入这个模块后，效果很好，稳定性也很好，且一直相安无事。直到2023年中的某一天，这个平静的情况被打破了。。。

ChromeDriver官方团队修改了发布方式，导致国内绝大部分的源都无法正确同步新版的ChromeDriver，作者使用的阿里源，也停留在了114版本上，无法继续更新。已向阿里源开发团队提交Issue后，已将新版ChromeDriver源同步完成，但是，已经无法按照新版源更换源地址实现下载了。

所以，经过作者研究源码，决定重新写一个下载模块，且基于阿里源为下载源！

## 解决问题

本模块可以看作是`webdriver_manager`模块的国内平替，为那些公司无法通过魔法手段连接github(比如作者公司T^T)
，和需要持续更新WebDriver的自动化测试同学们提供服务。

## 已实现功能

> 后续都会实现，如果有需求请及时提Issue

| Client  | Windows | MacOS |    Linux    |
|---------|:-------:|:-----:|:-----------:|
| Chrome  |    ✅    |   ✅   | ✅<br/>(未验证) |
| Firefox |    ✅    |   ✅   | ✅<br/>(未验证) |
| IE      |    ❎    |   ❎   |      ❎      |
| Edge    |    ❎    |   ❎   |      ❎      |

## 使用方法

安装：`pip install webdrivermanager_cn`

为简化使用方法，和替换成本，决定沿用`webdriver_manager`的使用风格：
如：

- ChromeDriver

```python
from webdrivermanager_cn.chrome import ChromeDriverManager

driver_path = ChromeDriverManager().install()
```

- Geckodriver

```python
from webdrivermanager_cn.geckodriver import GeckodriverManager

driver_path = GeckodriverManager().install()
```

## 其他

如果在使用过程中有任何问题，欢迎提Issue，会在第一时间处理！
