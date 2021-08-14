### 查看所有java进程的线程数

```shell
for pid in $(ps -ef|grep -v grep|grep java|awk '{print $2}');do echo ${pid} > /tmp/a.txt ;cat /proc/${pid}/status|grep Threads > /tmp/b.txt;paste /tmp/a.txt /tmp/b.txt;done|sort -k3 -rn

20104	Threads:	1823
26765	Threads:	643
11976	Threads:	581
7407	Threads:	516
```
### 检测僵尸进程
```shell
ps -e -o stat,ppid,pid,cmd|egrep '^[Zz]'|awk '{print $2}'|xargs kill -9
```

### 获取CPU或内存占用最高的进程
```shell
ps aux|head -1;ps aux|sort -k3 -rn|head -10

ps aux|head -1;ps aux|sort -k4 -rn|head -10

```

### 网络监控工具mtr

### 进程监控工具
1. ps
2. top
3. lsof
   1. lsof filename
   2. lsof -p PID
   3. lsof-i tcp:8080
4. pgrep
   1. pgrep -lo nginx
   2. pgrep -l -G root 

### 内存
```shell
vmstat 10 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0 122880 6848064 410596 25345500    0    0     1   138    0    0  2  0 97  0  0
 0  0 122880 6846764 410596 25345784    0    0     0   990 18909 28572  5  2 94  0  0
```
各列含义：
- r 运行和等待CPU时间片的进程数。
- b 等待资源的进程数，如正在等待I/O、内存交换等。
- swapd 切换到内存交换区的内存数量（以KB为单位）。
- free 当前空闲的物理内存数量（以KB为单位）。
- buff buffers cache的内存数量，一般对块设备的读写才需要缓冲。
- cache page cached的内存数量，一般作为文件系统cached，频繁访问的文件都会被cached。
- si 由磁盘调入内存，也就是内存进入内存交换区的数量。
- so 由内存调入磁盘，也就是内存交换区进入内存的数量。如果si、so的值长期不为0，则表示系统内存不足。
- bi 从块设备读入数据的总量（即读磁盘）（KB/s）。
- bo 写入到块设备的数据总量（即写磁盘）（KB/s）。这里设置的bi+bo参考值为1000，如果超过1000，而且wa值较大，则表示系统磁盘I/O有问题，应该考虑提高磁盘的读写性能。
- in 在某一时间间隔中观测到的每秒设备中断数。
- cs 每秒产生的上下文切换次数。这两个值越大，由内核消耗的CPU时间会越多。
- us 用户进程消耗的CPU时间百分比。如果长期大于50%，就需要考虑优化程序或算法。
- sy 内核进程消耗的CPU时间百分比。根据经验，us+sy的参考值为80%。
- id CPU处在空闲状态的时间百分比。
- wa I/O等待所占用的CPU时间百分比。根据经验，wa的参考值为20%
