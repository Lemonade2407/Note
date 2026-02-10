- 面向方面（Aspect）编程
- 引入AOP依赖
# 应用
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
		long endTime = System.currentTimeMillis();
		log.info("方法{}执行耗时：{}ms",pjp.getSignature(),endTime-beginTime);
		return result;
	}
}
```
# 核心概念
- 连接点JoinPoint：可以被AOP
- 通知Advice：
- 切入点PointCut：
- 切面Aspect：
- 目标对象Target：