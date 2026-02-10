- 线程的局部变量
- 用于在同一个线程中数据共享
```
public class threadLocal{
	private static final ThreadLocal<T> CURRENT_LOCAL = new ThreadLocal<>();
	
	public static set(T element){
		CURRENT_LOCAL.set(element);
	}
	public static get(){
		CURRENT_LOCAL.get();
	}
	public static remove(){
		CURRENT_LOCAL.remove();
	}
}
```