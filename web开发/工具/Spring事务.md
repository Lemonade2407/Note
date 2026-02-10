- 注解@Transactional
	- 属性1：rollbackFor = {Exception.class}//出现何种异常回滚事务
	- 属性2：propagation = Propagation.REQUIRED//当事务1被事务2调用时，事务1该如何控制事务
		- REQUIRED：有事务则加入，无事务则创建新事务
		- REQUIRES_NEW：创建新事物
- 配置事务管理日志级别
```
logging:
 level:
   org.springframework.jdbc.support.JdbcTransactionManager: debug
```