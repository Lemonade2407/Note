# JDBC
```
//注册驱动
Class.forName("驱动名");
//连接数据库
String url = "数据库地址";
String uername = "数据库用户名";
String password = "数据库密码";
Connection connection = DriveManager.getConnection(url,username,password);
//获取执行对象
Statement statement = connection.creatStatement();
//执行SQL(静态)
int i = statement.executeUpdata("SQL语句")
//执行预编译SQL(动态)
PreparedStatement pstmt = conn.prepareStatement("预编译SQL语句");
pstmt.setString(1,"");
ResultSet resultSet = pstmt.executeQuery();
//释放资源
statement.close();
connection.close();
```
# MyBatis
- 在