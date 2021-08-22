
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [nacos快速入门](#nacos快速入门)
- [Nacos Spring Cloud](#nacos-spring-cloud)
  - [使用配置中心](#使用配置中心)
  - [使用注册中心](#使用注册中心)
  - [服务提供者：demo](#服务提供者demo)
  - [服务消费者：demo-consumer](#服务消费者demo-consumer)
    - [使用 RestTemplate](#使用-resttemplate)
    - [使用 OpenFeign](#使用-openfeign)

<!-- /code_chunk_output -->

## nacos快速入门

启动nacos server：

```sh
unzip nacos-server-$version.zip 或者 tar -xvf nacos-server-$version.tar.gz
cd nacos/bin
sh startup.sh -m standalone
```

服务注册：

```sh
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'
```

服务发现：

```sh
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'
```

发布配置:

```sh
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"
```

获取配置：

```sh
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

控制台：<http://127.0.0.1:8848/nacos>， 用户名密码都是 nacos

## Nacos Spring Cloud

添加相关依赖，pom文件：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.3.5.RELEASE</version>
    <relativePath/> 
</parent>

<properties>
    <java.version>1.8</java.version>
    <spring-cloud.version>Hoxton.SR12</spring-cloud.version>
    <spring-cloud-alibaba.version>2.2.6.RELEASE</spring-cloud.version>
</properties>


<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-alibaba-dependencies</artifactId>
             <version>${spring-cloud-alibaba.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 使用配置中心

```properties
spring.cloud.nacos.config.server-addr=127.0.0.1:8848
spring.application.name=demo
spring.cloud.nacos.config.file-extension=properties
```

在 Nacos Spring Cloud 中，dataId 的完整格式如下：

```properties
${prefix}-${spring.profiles.active}.${file-extension}
```

- prefix 默认为 spring.application.name 的值，也可以通过配置项 spring.cloud.nacos.config.prefix来配置。
- spring.profiles.active 即为当前环境对应的 profile，详情可以参考 Spring Boot文档。 注意：当 spring.profiles.active 为空时，对应的连接符 - 也将不存在，dataId 的拼接格式变成 ${prefix}.${file-extension}
- file-exetension 为配置内容的数据格式，可以通过配置项 spring.cloud.nacos.config.file-extension 来配置。目前只支持 properties 和 yaml 类型。

通过 Spring Cloud 原生注解 @RefreshScope 实现配置自动更新：

```java
@RestController
@RequestMapping("/config")
@RefreshScope
public class ConfigController {

    @Value("${useLocalCache:false}")
    private boolean useLocalCache;

    @RequestMapping("/get")
    public boolean get() {
        return useLocalCache;
    }
}
```

首先通过调用 Nacos Open API 向 Nacos Server 发布配置：dataId 为 demo.properties，内容为 useLocalCache=true

```sh
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=demo.properties&group=DEFAULT_GROUP&content=useLocalCache=true"
```

测试效果：

```sh
# 返回内容是 true
curl http://localhost:8080/config/get
```

修改内容为 false:

```sh
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=demo.properties&group=DEFAULT_GROUP&content=useLocalCache=false"
```

测试效果：

```sh
# 返回内容是 false
curl http://localhost:8080/config/get
```

### 使用注册中心

### 服务提供者：demo

pom文件：

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    <exclusions>
        <exclusion>
            <groupId>com.alibaba.nacos</groupId>
            <artifactId>nacos-client</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>com.alibaba.nacos</groupId>
    <artifactId>nacos-client</artifactId>
    <version>2.0.3</version>
</dependency>
```

配置文件：

```properties
spring.application.name=demo
server.port=8070
spring.cloud.nacos.discovery.server-addr=localhost:8848
```

简单的api，echo：加上@EnableDiscoveryClient

```java
@SpringBootApplication
@EnableDiscoveryClient
public class NacosDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(NacosDemoApplication.class, args);
    }

    @RestController
    class EchoController {
        @RequestMapping(value = "/echo/{string}", method = RequestMethod.GET)
        public String echo(@PathVariable String string) {
            return "Hello Nacos Discovery " + string;
        }
    }
}
```

启动成功后，nacos 控制台服务列表查看是否注册成功。

### 服务消费者：demo-consumer

pom文件：

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    <exclusions>
        <exclusion>
            <groupId>com.alibaba.nacos</groupId>
            <artifactId>nacos-client</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>com.alibaba.nacos</groupId>
    <artifactId>nacos-client</artifactId>
    <version>2.0.3</version>
</dependency>
```

配置文件：

```properties
spring.application.name=demo-consumer
server.port=8080
spring.cloud.nacos.discovery.server-addr=192.168.101.2:8848
```

#### 使用 RestTemplate

```java
@SpringBootApplication
@EnableDiscoveryClient
public class NacosDemoApplication {


    @LoadBalanced
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    public static void main(String[] args) {
        SpringApplication.run(NacosDemoApplication.class, args);
    }

    @RestController
    class EchoController {
        @Autowired
        private RestTemplate restTemplate;

        @RequestMapping(value = "/echo/{str}", method = RequestMethod.GET)
        public String echo(@PathVariable String str) {
            return restTemplate.getForObject("http://demo/echo/" + str, String.class);
        }
    }
}
```

#### 使用 OpenFeign

pom文件加上 Feign 依赖

```xml

<dependency>
     <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

定义 Demo 服务的 Feign 接口：

```java
@FeignClient(value = "demo")
public interface DemoFeign {

    @RequestMapping(value = "/echo/{str}", method = RequestMethod.GET)
    String echo(@PathVariable String str);
}
```

使用 DemoFeign 调用 demo 服务：

```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class NacosDemoApplication {


    @LoadBalanced
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    public static void main(String[] args) {
        SpringApplication.run(NacosDemoApplication.class, args);
    }

    @RestController
    class EchoController {

        @Autowired
        DemoFeign demoFeign;


        @RequestMapping(value = "/echo/{str}", method = RequestMethod.GET)
        public String echo(@PathVariable String str) {
            return demoFeign.echo(str);
        }
    }
}
```
