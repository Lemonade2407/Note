# 使用步骤
- 引入依赖和配置文件logback.xml
- 定义日志记录对象Logger
`private static final Logger log=LoggerFactory.getLogger(LogTest.class)`
# 配置详解
- 配置输出的位置
	- 控制台输出:```
	```
	<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
		<encoder class = "ch.qos.logback.classic.encoder.PatternLayoutEncoder">
			//输出格式%d表示日期%thread表示线程名
			<pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread]%-5level %logger{50}-%msg%n</pattern>
		</encoder>
	</appender>
	```
	- 文件输出:
  ```
	<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<rollingPolicy>
			//文件名，%i表示序列号
			<FileNamePattern>filepath-%d{yyyy-MM-dd}-%i.log</FilenamePattern>
			//最多保留的文件数量
			<MaxHistory>30</MaxHistory>
			//最大文件大小
			<maxFileSize>10MB</maxFileSize>
		</rollingPolicy>
		<encoder class = "ch.qos.logback.classic.encoder.PatternLayoutEncoder">
				//输出格式%d表示日期%thread表示线程名
				<pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread]%-5level %logger{50}-%msg%n</pattern>
			</encoder>
	</appender>
  ```
- 日志开关
```
	<root level ="ALL">//ALL是开启OFF是关闭
		<appender-ref ref = "STDOUT" />
		<appender-ref ref = "FILE" />
	</root>
```
# 日志级别
- trace
- debug
- info
- warn
- error