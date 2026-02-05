# 使用步骤
- 引入依赖和配置文件logback.xml
- 定义日志记录对象Logger
`private static final Logger log=LoggerFactory.getLogger(LogTest.class)`
# 配置详解
- 配置输出的位置
	- 控制台输出:```
	  ```<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">...</appender>
	  ```
	- 文件输出:```<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">...</appender>```
- 日志开关
	```
	<root level ="ALL">//ALL是开启OF是关闭
		<appender-ref ref = "STDOUT" />
		<appender-ref ref = "FILE" />
	</root>
	```
	
# 方法