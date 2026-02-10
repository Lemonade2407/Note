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
	- 执行顺序：默认按字母排序（Before正序，After倒序）。可用@Order(数字)控制顺序（Before正序，After倒序）
- 切入点PointCut：匹配连接点的条件，通知仅在切入点执行时被应用
	- @Pointcut("切入点表达式")public void pt(){}，可以抽取公共表达式。
	- 切入点表达式：决定哪些方法需要加入通知
		- *通配单层，..通配多层
		- execution(返回值 包名.类名.方法名(方法参数))：根据方法的签名来匹配
		- 基于接口描述，而不是实现类
		- @annotation(...)：根据注解匹配
		- 自定义注解，将注解标记在所需类上
		- ```
		  @Target(ElementType.METHOD)
		  @Retention(RetentionPolicy.RUNTIME)
		  public @interface LogOperation{
		  }
		  ```
		
- 切面Aspect：通知与切入点
- 目标对象Target：通知的应用对象