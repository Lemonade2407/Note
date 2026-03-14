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
- 设置响应数据
```
public string response(HttpServletResponse response)throws IOException{
	//设置状态码(一般不需手动指定)
	response.setStatus(401);
	//设置响应头(一般不需手动指定)
	response.setHeader("key","value");
	//设置响应体
	response.getWriter().write("<h1>hello response</h1>");
}
或者
public ResponseEntity<String> response(){
	return ResponseEntity
		.status(401)
		.header("key","value")
		.body("<h1>hello response</h1>")
}
```
- 请求头：
- 前缀：