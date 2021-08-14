### 特点
Arthas可以帮助你解决以下问题：

1. 这个类从哪个 jar 包加载的？为什么会报各种类相关的 Exception？
2. 我改的代码为什么没有执行到？难道是我没 commit？分支搞错了？
3. 遇到问题无法在线上 debug，难道只能通过加日志再重新发布吗？
4. 线上遇到某个用户的数据处理有问题，但线上同样无法 debug，线下无法重现！
5. 是否有一个全局视角来查看系统的运行状况？
6. 有什么办法可以监控到JVM的实时运行状态？
7. 怎么快速定位应用的热点，生成火焰图？

### 如何使用
Arthas可以多种方式使用：
1. 本地直接运行：arthas-boot.jar 
2. Web Console：arthas-tunnel-server
3. 项目依赖：arthas-spring-boot-starter
4. 容器配置

### 命令大全

|NAME         |DESCRIPTION|
|:------------|:---|                                                           
|help         |Display Arthas Help                                                   
|keymap       |Display all the available keymap for the specified connection.        
|sc           |Search all the classes loaded by JVM                                  
|sm           |Search the method of classes loaded by JVM                            
|classloader  |Show classloader info                                                 
|jad          |Decompile class                                                       
|getstatic    |Show the static field of a class                                      
|monitor      |Monitor method execution statistics, e.g. total/success/failure count, average rt, fail rate, etc. 
|stack        |Display the stack trace for the specified class and method            
|thread       |Display thread info, thread stack                                     
|trace        |Trace the execution time of specified method invocation.              
|watch        |Display the input/output parameter, return object, and thrown excepti on of specified method invocation 
|tt           |Time Tunnel                                                           
|jvm          |Display the target JVM information                                    
|perfcounter  |Display the perf counter information.                                 
|ognl         |Execute ognl expression.                                              
|mc           |Memory compiler, compiles java files into bytecode and class files in memory. 
|redefine     |Redefine classes. @see Instrumentation#redefineClasses(ClassDefinition...)  
|retransform  |Retransform classes. @see Instrumentation#retransformClasses(Class...) 
|dashboard    |Overview of target jvm's thread, memory, gc, vm, tomcat info.         
|dump         |Dump class byte array from JVM                                        
|heapdump     |Heap dump                                                             
|options      |View and change various Arthas options                                
|cls          |Clear the screen                                                      
|reset        |Reset all the enhanced classes                                        
|version      |Display Arthas version                                                
|session      |Display current session information                                   
|sysprop      |Display, and change the system properties.                            
|sysenv       |Display the system env.                                               
|vmoption     |Display, and update the vm diagnostic options.                        
|logger       |Print logger info, and update the logger level                        
|history      |Display command history                                               
|cat          |Concatenate and print files                                           
|base64       |Encode and decode using Base64 representation                         
|echo         |write arguments to the standard output                                
|pwd          |Return working directory name                                         
|mbean        |Display the mbean information                                         
|grep         |grep command for pipes.                                               
|tee          |tee command for pipes.                                                
|profiler     |Async Profiler. https://github.com/jvm-profiling-tools/async-profiler 
|stop         |Stop/Shutdown Arthas server and exit the console.
