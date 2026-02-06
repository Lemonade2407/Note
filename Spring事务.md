- 注解@Transactional
	- 属性1：rollbackFor = {Exception.class}//rollbackFor代表出现何种异常回滚事务
- 配置事务管理日志级别
```
logging:
 level:
   org.springframework.jdbc.support.JdbcTransactionManager: debug
```