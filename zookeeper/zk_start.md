## quick start
### 安装
```sh
# 下载并解压到指定目录
/Users/gumengqin/Downloads/tools/apache-zookeeper-3.6.3-bin

# 配置文件,修改datedir
mv conf/zoo_sample.conf conf/zoo.conf
vi conf/zoo.conf
dataDir=/Users/gumengqin/Downloads/tools/zkdata

# zkServer.sh启动
cd bin
./zkServer.sh
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /Users/gumengqin/Downloads/tools/apache-zookeeper-3.6.3-bin/bin/../conf/zoo.cfg
Usage: ./zkServer.sh [--config <conf-dir>] {start|start-foreground|stop|version|restart|status|print-cmd}

# 可见新版本更友好，可以有各种选项了，start吧
./zkServer.sh start

## start是后台启动，即使重启终端也不会关闭，查看状态
./zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /Users/gumengqin/Downloads/tools/apache-zookeeper-3.6.3-bin/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: standalone
```
### zkClient使用

```shell
# 启动客户端
bin/zkCli.sh -server 127.0.0.1:2181

# help查看所有命令
[zk: localhost:2181(CONNECTED) 0] help
ZooKeeper -server host:port -client-configuration properties-file cmd args
	addWatch [-m mode] path # optional mode is one of [PERSISTENT, PERSISTENT_RECURSIVE] - default is PERSISTENT_RECURSIVE
	addauth scheme auth
	close 
	config [-c] [-w] [-s]
	connect host:port
	create [-s] [-e] [-c] [-t ttl] path [data] [acl]
	delete [-v version] path
	deleteall path [-b batch size]
	delquota [-n|-b] path
	get [-s] [-w] path
	getAcl [-s] path
	getAllChildrenNumber path
	getEphemerals path
	history 
	listquota path
	ls [-s] [-w] [-R] path
	printwatches on|off
	quit 
	reconfig [-s] [-v version] [[-file path] | [-members serverID=host:port1:port2;port3[,...]*]] | [-add serverId=host:port1:port2;port3[,...]]* [-remove serverId[,...]*]
	redo cmdno
	removewatches path [-c|-d|-a] [-l]
	set [-s] [-v version] path data
	setAcl [-s] [-v version] [-R] path acl
	setquota -n|-b val path
	stat [-w] path
	sync path
	version 


[zk: localhost:2181(CONNECTED) 13] ls /
[zk_test, zookeeper]

[zk: localhost:2181(CONNECTED) 8] create /zk_test my_data
Created /zk_test

[zk: localhost:2181(CONNECTED) 9] ls /
[zk_test, zookeeper]

[zk: localhost:2181(CONNECTED) 10] get /zk_test
my_data

[zk: localhost:2181(CONNECTED) 12] get -s /zk_test
my_data
cZxid = 0x2
ctime = Sun May 16 17:28:05 CST 2021
mZxid = 0x2
mtime = Sun May 16 17:28:05 CST 2021
pZxid = 0x2
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 7
numChildren = 0

[zk: localhost:2181(CONNECTED) 13] set /zk_test junk

WATCHER::

WatchedEvent state:SyncConnected type:NodeDataChanged path:/zk_test

[zk: localhost:2181(CONNECTED) 15] get -s /zk_test
junk
cZxid = 0x2
ctime = Sun May 16 17:28:05 CST 2021
mZxid = 0x3
mtime = Sun May 16 17:33:00 CST 2021
pZxid = 0x2
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 4
numChildren = 0

[zk: localhost:2181(CONNECTED) 16] delete /zk_test

[zk: localhost:2181(CONNECTED) 17] ls /
[zookeeper]

```
### zooInspector
如果不习惯命令行zkClient，可以用可视化工具zooInspector。
```shell
# 下载并解压到指定目录
/Users/gumengqin/Downloads/tools/ZooInspector/

# 运行
cd build
java -jar zookeeper-dev-ZooInspector.jar
```
