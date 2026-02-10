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
	- @Around：目标方法前、后都被执行，返回值必须为Object
	- @Before：目标方法前执行
	- @After：目标方法后执行
	- @AfterReturning：目标方法后执行，有异常不执行
	- @AfterThrowing：异常后执行
- 切入点PointCut：匹配连接点的条件，通知仅在切入点执行时被应用
	- @Pointcut("切入点表达式")public void pt(){}，可以抽取公共表达式。
- 切面Aspect：通知与切入点
- 目标对象Target：通知的应用对象