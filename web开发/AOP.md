- 面向方面（Aspect）编程
- 用于定位耗时较长的方法
```
@Slf4j
@Aspect
@Component
public class RecordTimeAspect{
	@Around("execution(...)")
	public Object recordTime(ProceedingJoinPoint pjp){
		long beginTime = System.currentTimeMillis();
		Object result = pjp.proceed();
		long endTime = 
	}
}
```