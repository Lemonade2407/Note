# 坐标
- 是资源的唯一标识，通过该坐标可以唯一定位资源位置
- 使用坐标来定义项目或引入项目中需要的依赖
- 组成：
	- groupId：隶属组织名称（一般为域名反写）
	- artifactId：项目名称（通常为模块名称）
	- version：当前版本号
		- SNAPSHOT：开发中版本
		- RELEASE：发行版本
# 依赖
- 项目运行所需要的jar包
- 配置依赖：
	- 在pom.xml中编写`<dependencies>`标签
	- 在`<dependencies>`标签中加入`<dependency>`
	- 在`<dependency>`标签中定义坐标
- 排除依赖：
	- 在对应`<dependency>`标签中定义`<exclusions>`
	- 在`<exclusions>`标签中加入`<exclusion>`
	- 在`<exclusion>`中定义要排除的依赖的坐标（不用写版本号）
- 依赖范围：
	- 通过`<scope>`设置作用范围，在`<dependency>`标签中定义

| scope值      | 主程序有效 | 测试程序有效 | 是否参与打包运行 |
| ----------- | ----- | ------ | -------- |
| compile(默认) | √     | √      | √        |
| test        |       | √      |          |
| provided    | √     | √      |          |
| runtime     |       | √      | √        |

# 生命周期
- clean：清理之前操作的残余文件
- default：核心
	- compile：编译
	- test：测试
	- package：打包
	- install：安装项目到本地仓库
- site：
- 删除残留文件：命令行`del /s *.lastUpdate`
# 分模块设计
- 按功能分
- 按层分
- 按功能+层分
- 每一个部分单独创建Maven模块，在management模块中引入其他部分依赖
# 继承
- `<parent>父工程</parent>`
- 创建parent模块作为项目父工程，打包方式改为pom`<packaging>pom</packaging>`
- 子工程中配置父工程依赖
```
<parent>
 <groupId></groupId>
 <artifactId>parent</artifactId>
 <version>...</version>
 <relativePath>相对路径</relativePath>
</parent>
```
# 版本锁定
- 在父工程中通过`<dependencyManagement>`统一管理依赖版本
```
父工程
<dependencyManangement>
	<dependencies>
		<groupId>...</groupId>
		<artifactId>...</artifactId>
		<version>...</version>
	</dependencies>
</dependencyManagement>
子工程仍需引用依赖，但无需配置版本
<dependencies>
	<groupId>...</groupId>
	<artifactId>...</artifactId>
</dependencies>
```
- 优化：使用自定义属性
```
<properties>


```