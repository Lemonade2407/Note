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
- 连接点JoinPoint：可以被AOP控制的方法
- 通知Advice：重复的逻辑（体现为一个方法）
- 切入点PointCut：匹配连接点的条件，通知仅在切入点执行时被应用
- 切面Aspect：描述通知与切入点的对应关系
- 目标对象Target：通知的应用对象