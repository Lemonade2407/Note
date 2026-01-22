- 获取请求体
```
public string request(HttpServletRequest request){
	//获取请求方式
	String method = request.getMethod();
	//获取url地址
	String url = request.getRequestURL().toString();
	//获取请求协议
	String protocol = request.getProtocol
	//获取请求参数
	String name = request.getParameter("name")
	//获取请求头
	String accept = request.getHeader("Accept")
}
```
- 设置