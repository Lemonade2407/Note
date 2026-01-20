# Maven
- 坐标：是资源的唯一标识，通过该坐标可以唯一定位资源位置
	- 使用坐标来定义项目或引入项目中需要的依赖
	- 组成：
		- groupId：隶属组织名称（一般为域名反写）
		- artifactId：项目名称（通常为模块名称）
		- version：当前版本号
			- SNAPSHOT：开发中版本
			- RELEASE：发行版本
- 依赖：项目运行所需要的jar包
	- 配置依赖：
		- 在pom.xml中编写`<dependencies>`标签
		- 在`<dependencies>`标签中加入`<dependency>`
		- 在`<dependency>`标签中定义坐标
	- 排除依赖：
		- 在对应`<dependency>`标签中定义`<exclusions>`
		- 在`<exclusions>`标签中加入`<exclusion>`
		- 在`<exclusion>`中定义要排除的依赖的坐标（不用写版本号）
- 生命周期
	- clean：清理之前操作的残余文件
	- default：核心
		- compile：编译
		- test：测试
		- package：打包
		- install：安装项目到本地仓库
	- site：
# 测试
- 阶段划分：单元测试（白）->集成测试（灰）->系统测试（黑）->验收测试（黑）
- 测试方法：白盒测试、黑盒测试以及灰盒测试
## 单元测试
- 引入JUnit依赖
- 在test/java目录下创建测试类
- 声明@Test注解并编写测试方法
- 命名规范：xxxxTest，方法为public void
### 断言
- 给出正确答案，判断业务逻辑是否正确

| 断言方法                                                                | 作用                  |
| ------------------------------------------------------------------- | ------------------- |
| `Assertions.assertEquals(Object exp,Object act,String msg)`         | 两值是否相等，不相等则报错       |
| `Assertions.assertNotEquals(Object unexp,Object act,String msg)`    | 两值是否不相等，相等则报错       |
| `Assertions.assertNull(Object act,String msg)`                      | 检查对象是否为Null，否报错     |
| `Assertions.assertNotNull(Object act,String msg)`                   | 检查对象是否为Null，是报错     |
| `Assertions.assertTrue(boolean condition,String msg)`               | 检查条件是否为true，否报错     |
| `Assertions.assertFalse(boolean condition,String msg)`              | 检查条件是否为false，否报错    |
| `Assertions.assertThrows(Class expType,Executable exec,String msg)` | 检查程序抛出的异常是否符合预期，否报错 |
