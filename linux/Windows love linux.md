# Windows 10 安装 linux 子系统

## 第1步：卸载之前的linux子系统

```sh
lxrun /uninstall /full
```

## 第2步：启用高级特性：Microsoft-Windows-Subsystem-Linux

```sh
# 检查是否启用
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
# 启用
Enable-WindowsOptionalFeature -FeatureName "Microsoft-Windows-Subsystem-Linux" -Online -NoRestart:$False
```

## 第3步：下载appx ubuntu

```sh
Invoke-WebRequest  -Uri "https://aka.ms/wsl-ubuntu-1804"  -OutFile "~\Ubuntu18.04onWindows.appx"  -UseBasicParsing

Add-AppxPackage -Path "~\Ubuntu18.04onWindows.appx"
```

也可以在应用商店下，只不过我的应用商店没法联网。或者去ubuntu官网下：<https://aka.ms/wslubuntu2004>

## 第4步：启动Ubuntu

```sh
# 按 Win 键显示开始菜单，点击Ubuntu，报错如下：

Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x800701bc
Error: 0x800701bc WSL 2 ?????????????????? https://aka.ms/wsl2kernel

Press any key to continue...
```

百度一番，找到以下帖子：<https://github.com/microsoft/WSL/issues/5393> 。有人回帖：go to <https://aka.ms/wsl2kernel>. 转过去下载wsl_update_x64.msi,安装。

没解决，去Stack Overflow 搜，有人说主板开启 Intel VT-x，重启按 DELTE键进入主板，一顿操作按 F10保存

然后再启用虚拟化高级特性：

```sh
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

再重启，终于解决了，Enter new UNIX username: cafebabe，密码：白日依山尽

## 参考资料

<https://wiki.ubuntu.com/WSL>

<https://docs.microsoft.com/zh-cn/windows/wsl/install-win10>

<https://www.how2shout.com/how-to/solve-wslregisterdistribution-failed-with-error-0x800701bc.html>

## 第5步：切换apt源

```sh
su root
cd /etc/apt
cp sources.list sources.list.bak
vi sources.list

deb https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse

## Not recommended
# deb https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse


apt-get update
```
