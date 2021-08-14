## IO基础
### Linux网络IO模型
Unix网络编程中对Unix IO模型的分类：
- 阻塞IO
- 非阻塞IO
- IO复用
- 信号驱动IO
- 异步IO

### epoll对比select的优点：
1. epoll支持一个进程打开的FD不受限制（受限于最大文件句柄数，cat /proc/sys/fs/file-max ）。
2. epoll的IO效率不会随着FD的数目增加而线性下降（基于callback回调函数实现，而select是顺序轮询）。
3. epoll使用mmap加速内核与用户空间的消息传递。
4. epoll的API更加简洁。

### Java IO演进
- jdk1.4之前，bio
- jdk1.4引入java.nio
  - ByteBuffer
  - Pipe
  - Channel：ServerSocketChannel，SocketChannel，FileChannel
  - 多种字符集编码解码
  - selector
  - 正则表达式类库   
- jdk1.7 NIO2.0
  - 批量获取文件属性的API
  - 提供AIO支持 
  - 完善Channel的功能

### 传统BIO编程
传统BIO编程模型：由一个acceptor监听所有连接，收到连接请求后，为每个客户端请求创建一个新的线程进行处理。这就是典型的 **one thread per connect**。

主程序无限循环，accept成功后创建处理线程：
```java
public class TimeServer {
    private static final int port = 8088;

    public static void main(String[] args) throws IOException {
        ServerSocket server = null;
        try {
            server = new ServerSocket(port);
            System.out.println("The time server is start in port : " + port);
            Socket socket = null;
            while (true) {
                socket = server.accept();
                new Thread(new TimeServerHandler(socket));
            }
        } finally {
            if (server != null) {
                System.out.println("The time server close");
                server.close();
                server = null;
            }
        }
    }
}
```
处理线程：
```java
public class TimeServerHandler implements Runnable {
    private Socket socket;

    public TimeServerHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        BufferedReader in = null;
        PrintWriter out = null;
        try {
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);
            String currentTime;
            String body;
            while (true) {
                body = in.readLine();
                if (body == null) {
                    break;
                }
                System.out.println("The time server receive order: " + body);
                currentTime = "QUERY TIME ORDER".equalsIgnoreCase(body) ? LocalDateTime.now().toString() : "BAD ORDER";
                out.println(currentTime);
            }
        } catch (IOException e) {
            if (in != null) {
                try {
                    in.close();

                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }
            }
            if (out != null) {
                out.close();
            }
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }
                socket = null;
            }
        }
    }
}
```
### NIO编程
Java NIO编程的一般步骤：
1. 打开通道ServerSocketChannel
2. 设置非阻塞并绑定端口监听
3. 创建selector，创建reactor线程
4. 注册通道，监听accept事件
5. selector轮询就绪key
6. 如果有accept事件，调用accpet()建立连接
7. 设置客户端socket非阻塞，并注册读事件
8. 读取客户端数据到read缓冲区
9. 对read缓冲区编解码，将消息投递到业务线程中
10. 将业务数据编解码，发送给客户端

```java
public class TimeServer {
    private static final int port = 8088;

    public static void main(String[] args) {
        MultiplexerTimeServer timeServer = new MultiplexerTimeServer(port);
        new Thread(timeServer, "NIO-MultiplexerTimeServer-001").start();
    }
}
```
```java
public class MultiplexerTimeServer implements Runnable {
    private Selector selector;

    public MultiplexerTimeServer(int port) {
        try {
            selector = Selector.open();
            ServerSocketChannel serverChannel = ServerSocketChannel.open();
            serverChannel.configureBlocking(false);
            serverChannel.socket().bind(new InetSocketAddress(port), 1024);
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);
            System.out.println("The time server is start in port: " + port);
        } catch (IOException e) {
            System.exit(1);
        }
    }

    @Override
    public void run() {
        while (true) {
            try {
                selector.select(1000);
                Set<SelectionKey> selectedKeys = selector.selectedKeys();
                Iterator<SelectionKey> it = selectedKeys.iterator();
                SelectionKey key;
                while (it.hasNext()) {
                    key = it.next();
                    it.remove();
                    try {
                        handleInput(key);
                    } catch (Exception e) {
                        if (key != null) {
                            key.cancel();
                            if (key.channel() != null) {
                                key.channel().close();
                            }
                        }
                    }
                }
            } catch (Throwable t) {
                t.printStackTrace();
            }
        }
    }

    private void handleInput(SelectionKey key) throws IOException {
        if (key.isValid()) {
            //新连接
            if (key.isAcceptable()) {
                ServerSocketChannel ssc = (ServerSocketChannel) key.channel();
                SocketChannel sc = ssc.accept();
                sc.configureBlocking(false);
                //监听新连接的读事件
                sc.register(selector, SelectionKey.OP_READ);
            }
            //读事件
            if (key.isReadable()) {
                SocketChannel sc = (SocketChannel) key.channel();
                ByteBuffer readBuffer = ByteBuffer.allocate(1024);
                int readBytes = sc.read(readBuffer);
                if (readBytes > 0) {
                    readBuffer.flip();
                    byte[] bytes = new byte[readBuffer.remaining()];
                    readBuffer.get(bytes);
                    String body = new String(bytes, StandardCharsets.UTF_8);
                    System.out.println("The time server receive order: " + body);
                    String currentTime = "QUERY TIME ORDER".equalsIgnoreCase(body) ? LocalDateTime.now().toString() : "BAD ORDER";
                    //写入
                    doWrite(sc, currentTime);
                } else if (readBytes < 0) {
                    key.channel();
                    sc.close();
                }
            }
        }
    }

    private void doWrite(SocketChannel channel, String response) throws IOException {
        if (response != null && response.trim().length() > 0) {
            byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
            ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);
            writeBuffer.put(bytes);
            writeBuffer.flip();
            channel.write(writeBuffer);
        }
    }
}
```