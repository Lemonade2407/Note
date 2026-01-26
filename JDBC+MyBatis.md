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
- 在resources目录下的application.proprietaries中配置
```
//数据库连接信息
spring.datasource.url = 
spring.datasource.driver-class-name = 
spring.datasource.username = 
spring.datasource.password = 
//日志输出信息
mybatis.configuration.log-impl = org.apache.ibatis.logging.stdout.StdOutImpl
```
- 创建Mapper
```
@Mapper//自动为接口创建bean对象
public interface Mapper{
}
```
- 增删改查
```
@Insert("insert into user(username,password,name,age)values(#{username},#{password},#{name},#{age})")
public void insert(User user);

@Delete("delete from user where id = #{id}")
public void deleteById(Integer id);

@Update("update user set username=#{username},password=#{password},name#{name},age=#{age}where id=#{id}")
public void update(User user);

@Select("select * from user where username=#{username} and password=#{password}")
public User findByUsernameAndPassword(@Param("username")String username,@Param("password")String password);//基于springboot框架可以省略@Param
```
- XML映射配置
	- xml文件预Mapper接口名称一致，