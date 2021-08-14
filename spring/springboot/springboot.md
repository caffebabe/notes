**目录**
- [SpringApplication类](#springapplication类)
  - [Application events](#application-events)
- [配置](#配置)
- [日志](#日志)
- [Web](#web)

# SpringApplication类

## Application events
- **ApplicationStartingEvent**：listeners and initializers注册完成。
- **ApplicationEnvironmentPreparedEvent**：Environment已准备，准备创建ApplicationContext。
- **ApplicationContextInitializedEvent**：ApplicationContext创建完成，开始加载bean定义。
- **ApplicationPreparedEvent**：bean加载完成，开始调用refresh。
- **WebServerInitializedEvent**：WebServer完成。 
- **ContextRefreshedEvent**：refresh调用完成。
- **ApplicationStartedEvent**：应用启动成功，但runners还没调用。
- **AvailabilityChangeEvent**：LivenessState.CORRECT
- **ApplicationReadyEvent**：runners调用完成。
- **AvailabilityChangeEvent**：ReadinessState.ACCEPTING_TRAFFIC 
- **ApplicationFailedEvent**：出现异常会发出错误事件。

# 配置

**配置属性加载顺序**

1. Default properties (SpringApplication.setDefaultProperties).
2. @PropertySource annotations on your @Configuration classes. 
3. Config data (such as application.properties files)
4. A RandomValuePropertySource that has properties only in random.*.
5. OS environment variables(eg: SPRING_APPLICATION_JSON='{"acme":{"name":"test"}}').
6. Java System properties (eg: -Dspring.application.json='{"acme":{"name":"test"}}').
7. JNDI attributes from java:comp/env.
8. ServletContext init parameters.
9. ServletConfig init parameters.
10. Properties from SPRING_APPLICATION_JSON (inline JSON embedded in an environment variable or system property).
11. Command line arguments(eg: --spring.application.json='{"acme":{"name":"test"}}').
12. properties attribute on your tests. Available on @SpringBootTest and the test annotations for testing a particular slice of your application.
13. @TestPropertySource annotations on your tests.
14. Devtools global settings properties in the $HOME/.config/spring-boot directory when devtools is active.

**配置文件的顺序如下**

1. Application properties packaged inside your jar (application.properties and YAML variants).
2. Profile-specific application properties packaged inside your jar (application-{profile}.properties and YAML variants).
3. Application properties outside of your packaged jar (application.properties and YAML variants).
4. Profile-specific application properties outside of your packaged jar (application-{profile}.properties and YAML variants).

**寻找配置文件的顺序**

1. The classpath root
2. The classpath /config package
3. The current directory
4. The /config subdirectory in the current directory
5. Immediate child directories of the /config subdirectory

**几个重要的配置：必须作为环境属性，一般设置为环境变量或命令行参数.**

- spring.config.name=配置文件名称
- spring.config.location=配置文件路径
- spring.profiles.active=激活的环境

**Configuration Trees**

Kubernetes can volume mount both ConfigMaps and Secrets.

As an example, let’s imagine that Kubernetes has mounted the following volume:
```
etc/
  config/
    myapp/
      username
      password
```
则应用可以这样导入这两个文件：
```properties
spring.config.import=optional:configtree:/etc/config/
```

**加密配置**

Spring Boot没有提供内置的属性值加密方法，但提供了钩子函数用于修改Environment中的属性值，可以实现**EnvironmentPostProcessor**。  

# 日志

默认日志输出格式：
```
时间 级别 进程号 --- [ 线程名] 类名 ：日志信息
```
默认日志级别为INFO，可以加启动参数--debug或--trace输出更细的日志；

默认日志输出到控制台，不写文件

**文件日志**
```properties
logging.file.name=spring.log
logging.file.path=/var/log
```
**日志级别**

```properties
logging.level.<logger-name>=<level> 
logging.level.root=warn
logging.level.org.springframework.web=debug
logging.level.org.hibernate=error

# 定义日志组
logging.group.tomcat=org.apache.catalina,org.apache.coyote,org.apache.tomcat
logging.level.tomcat=trace

# spring提供的日志组
logging.level.web=error
logging.level.sql=error
```

**第三方日志框架配置文件**

|  日志框架   | 配置文件  |
|  ----  | ----  |
| Logback  | logback.xml or logback-spring.xml |
| Log4j2  | log4j2.xml or log4j2-spring.xml |
| JUL | logging.properties |
|||

**带-spring的文件名才支持spring扩展：**
```xml
<springProfile name="!production">
	<!-- configuration to be enabled when the "production" profile is not active -->
</springProfile>

<springProperty scope="context" name="fluentHost" source="myapp.fluentd.host" defaultValue="localhost"/>
<appender name="FLUENT" class="ch.qos.logback.more.appenders.DataFluentAppender">
	<remoteHost>${fluentHost}</remoteHost>
</appender>
```

# Web
**Spring MVC自动配置:**
- **ContentNegotiatingViewResolver** and **BeanNameViewResolver** .
- Support for serving **static resources**, including support for WebJars.
- Automatic registration of **Converter**, GenericConverter, and **Formatter** beans.
- Support for **HttpMessageConverters**.
- Automatic registration of **MessageCodesResolver**.
- Static **index.html** support.
- Automatic use of a **ConfigurableWebBindingInitializer** bean.

**使用fastjson解析http request body**

Springboot 默认为 HttpMessageConverters 添加了MappingJackson2HttpMessageConverter，所以默认使用Jackson序列化。

要改成fastjson，只需覆盖配置 HttpMessageConverters 即可：

```java
@Configuration(proxyBeanMethods = false)
public class MyConfiguration {
    @Bean
    public HttpMessageConverters fastJsonHttpMessageConverters() {
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        SerializerFeature[] serializerFeatures = new SerializerFeature[]{SerializerFeature.WriteMapNullValue};
        fastJsonConfig.setSerializerFeatures(serializerFeatures);
        fastJsonConfig.setCharset(StandardCharsets.UTF_8);

        FastJsonHttpMessageConverter fastConverter = new FastJsonHttpMessageConverter();
        fastConverter.setFastJsonConfig(fastJsonConfig);

        return new HttpMessageConverters(fastConverter);
    }
}
```

