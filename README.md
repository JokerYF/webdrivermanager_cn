# WerDriverManagerCn

> 基于 [阿里源](https://www.npmmirror.com/)
> 开发，灵感来源：[webdriver_manager](https://githHub.com/SergeyPirogov/webdriver_manager)，向原作者致敬！

## 开发背景

作者是测开一枚，一直在公司默默无闻的做着自动化测试，偶然公司同事安利 `webdriver_manager`
这个模块可以有效解决Chrome频繁更新导致ChromeDriver无法使用的问题，可以直接更换国内源，解决默认为GitHub源而导致下载慢或者失败的问题。

自动化项目引入这个模块后，效果很好，稳定性也很好，且一直相安无事。直到2023年中的某一天，这个平静的情况被打破了。。。

ChromeDriver官方团队修改了发布方式，导致国内绝大部分的源都无法正确同步新版的ChromeDriver，作者使用的阿里源，也停留在了114版本上，无法继续更新。已向阿里源开发团队提交Issue后，已将新版ChromeDriver源同步完成，但是，已经无法按照新版源更换源地址实现下载了。

所以，经过作者研究源码，决定重新写一个下载模块，且基于阿里源为下载源！

## 解决问题

本模块可以看作是 `webdriver_manager` 模块的国内平替，为那些公司无法通过魔法手段连接GitHub(比如作者公司T_T)
，和需要持续更新WebDriver的自动化测试同学们提供服务。

## 已实现功能

> 后续都会实现，如果有需求请及时提Issue

| Client  | Windows | MacOS |    Linux    |
|:-------:|:-------:|:-----:|:-----------:|
| Chrome  |    ✅    |   ✅   |      ✅      |
| Firefox |    ✅    |   ✅   | ✅<br/>(未验证) |
|   IE    |    ❎    |   ❎   |      ❎      |
|  Edge   |    ✅    |   ✅   |      ✅      |

## 使用方法

### 安装升级

- 安装命令：`pip install webdrivermanager_cn`
- 在线升级：`pip install -U webdrivermanager_cn`

### 导入使用

为简化使用方法，降低替换成本，决定沿用`webdriver_manager`的使用风格：
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

- edge

```python
from webdrivermanager_cn.microsoft import EdgeWebDriverManager

driver_path = EdgeWebDriverManager().install()
```

## 全局变量

wdmcn也像wdm一样，内置了一些全局变量，后续会根据需求继续添加，具体请看`config.py`，这里简单列举一下。

- 日志功能

  - 日志功能默认关闭，可以通过`os.environ['WDM_LOG'] = 'true'`打开，默认为false
  - 日志等级，可以通过`os.environ['WDM_LOG_LEVEL'] = f'{logging.INFO}'`修改，默认等级为INFO
  - 自定义logger，可以通过导入`set_logger()`方法，将您自己的logger添加进来，则日志输出就会使用您的logger记录

- 定期清理旧的webdriver

  -
  如果您使用的wdmcn时间很长以后，webdriver会随着chrome等浏览器版本的迭代越来越多，现在可以默认删除无用的webdriver，可以使用`os.environ['WDM_CACHE_TIME'] = 5`
  设置，默认会清理5天前的webdriver，以减少磁盘占用。

## 其他

如果在使用过程中有任何问题，欢迎提Issue，会在第一时间处理！
