- 面向方面（Aspect）编程
- 用于定位耗时较长的方法
- 引入AOP依赖
```
@Slf4j
@Aspect
@Component
public class RecordTimeAspect{
	@Around("execution(...)")
	public Object recordTime(ProceedingJoinPoint pjp){
		long beginTime = System.currentTimeMillis();
		Object result = pjp.proceed();
		long endTime = System.currentTimeMillis();
		log.info("执行耗时：{}ms",endTime-beginTime);
	}
}
```