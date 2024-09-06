# EZ-ANDROID-AUTOMATOR

一个基于uiautomator2的安卓自动化框架项目

该框架能够实现对安卓设备的可视元素实现监视并执行自动化操作，框架本身功能强调多设备、多任务的调度，可以以良好的性能实现批量控制手机以高效的方式执行自动化操作。

项目仍然在早期开发阶段，文档和API接口并不稳定，欢迎贡献PR和提出Issue。

## 项目用途

该项目可用于：工作室搬砖、媒体矩阵、抢票、签到等

## 可用模块

本项目的核心库由开发者EnderTheCoder维护，保证第一优先级修复问题和提高代码质量。
其余派生任务类可能由于人力问题无法得到妥善维护，欢迎贡献PR。

以下模块由EnderTheCoder维护

| 模块                                               | 用途                               |
|--------------------------------------------------|----------------------------------|
| [app_file](ez_android_automator/app_file.py)     | 用于在root过的设备上实现自动化保存和恢复APP的登陆状态   |
| [client](ez_android_automator/client.py)         | 核心库，项目的大部分内容所在                   |
| [idm_task](ez_android_automator/idm_task.py)     | 一个简单的任务，用于向没有root的设备上传输文件并立即刷新相册 |
| [manager](ez_android_automator/manager.py)       | 任务调度器，用于向多设备分发多任务，实现异步调用和异常处理    |
| [damai_task](ez_android_automator/damai_task.py) | 大麦自动抢票脚本，如果需要使用需要自行编写一个简单的启动任务脚本 |

项目原本目的用于媒体矩阵，包含很多遗留的过时测试脚本和任务，请忽略以test_开头的文件。

## 切换adb模式方法

adb在开机的时候默认运行在usb模式下，我们无法通过ip地址连接到机器，所以需要切换到tcpip模式下。
手动切换可以使用命令

```shell
adb -s 机器序列号 tcpip 端口号
```

其中端口号默认为5555

如果要查询机器的序列号，使用命令

```shell
adb devices
```

若要使用自动切换请按照以下步骤进行

1. 启动黑盒子
2. 连接黑盒子的usb到电脑上
3. 按下模式切换按钮（切换后指示灯为蓝色）
4. 运行自动切换脚本make_all_usb_devices_tcpip.py
5. 按下模式切换按钮（切换后指示灯为绿色）
6. 登陆路由器管理界面查看手机ip（默认为192.168.3.1，密码123456）
