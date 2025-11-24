;结尾
不区分大小写
--或#单行注释，/ * * /多行注释
# SQL
## DDL(definition定义)
### 数据库操作
#### 查询
- 所有数据库：show database;
- 当前数据库：select database();
#### 创建
- create database [ if not exists ] 数据库名 [ default charset字符集 ]  [ collate排序规则 ];
  *==字符集建议utf8mb4==*
#### 删除
- drop database [ if not exists ] 数据库名;
#### 使用
- use 数据库名;
### 表操作
#### 查询
- 所有表：show tables;
- 表结构：desc 表名;(describe 描述)
- 建表语句：show create table 表名;
#### 创建
- create table 表名(
	字段 类型 [ comment 注释 ]，
	……
	) [ comment 表注释 ] ;

| 数值      | 大小    | 字符串     | 描述  | 日期       | 大小    | 格式                  |
| ------- | ----- | ------- | --- | -------- | ----- | ------------------- |
| int     | 4byte | char    | 定长  | date     | 3byte | yyyy-mm-dd          |
| float   | 4byte | varchar | 变长  | time     | 3byte | hh:mm:ss            |
| double  | 8byte | blob    | 二进制 | year     | 1byte | yyyy                |
| decimal | 4byte | text    | 字符串 | datetime | 8byte | yyyy-mm-dd hh:mm:ss |
*==字符串和日期型字段应包含在＂＂里==*
#### 修改
- 添加：alter table 表名 add 字段名 类型（长度） [ comment 注释 ]  [ 约束 ];
- 修改数据类型：alter table 表名 modify 字段名 新数据类型（长度）;
- 修改字段名和类型：alter table 表名 change 旧字段名 新字段名 类型（长度）[ comment 注释 ]  [ 约束 ];
- 删除字段：alter table 表名 drop 字段;
- 修改表名：alter table 表名 rename to 新表名;
#### 删除
- 删除表：drop table [ if exists ] 表名;
- 删除并重新创建表：turncate table 表名;
## DML(manipulation操作)
### 添加
- 指定字段添加：insert into 表名（字段1，字段2，……）value（值1，值2，……）;
- 所有字段添加：insert into  表名 value（值1，值2，……）;
- 批量添加：insert into 表名（字段1，字段2，……）value（值1，值2，……），（值1，值2，……），（值1，值2，……）;
		   insert into 表名 value（值1，值2，……），（值1，值2，……），（值1，值2，……）;
### 修改
- update 表名 set 字段名1=值1，字段名2=值2，…… [ where 条件 ] ;
   *==set 字段=null时删除字段==*
### 删除
- delete from 表名 [ where 条件 ]  ;
  *==无法删除字段==*
## DQL(query查询)
编写顺序：select---from---where---group by---having---order by---limit
执行顺序：from---where---group by---having---select---order by---limit
### 基础查询
- 多个字段：select 字段1，字段2，……from 表名;
		   select * from 表名;
- 设置别名：select 字段1 as 别名1，字段2 as 别名2 ……from 表名 as 别名;
- 去除重复：select distinct 字段列表 from 表名;
### 条件查询
- select 字段列表 from 表名 where 条件列表;

| 比较运算符          | 功能               | 逻辑运算符   | 功能  |
| -------------- | ---------------- | ------- | --- |
| ＞              |                  | and 或&& | 并且  |
| ＞＝             |                  | or或‖    | 或者  |
| ＜              |                  | not或！   | 取反  |
| ＜＝             |                  |         |     |
| ＝              |                  |         |     |
| ！＝或者＜＞         | 不等于              |         |     |
| between……and…… | （最小，最大）包含边界值     |         |     |
| in（……）         | in后的值任一匹配        |         |     |
| like 占位符       | 模糊匹配，_匹配单个，%匹配多个 |         |     |
| is null        |                  |         |     |
### 分组查询
- 聚合函数：select 聚合函数（字段列表）from 表名;

| 聚合函数      | 功能   |
| --------- | ---- |
| count（字段） | 统计数量 |
| max（字段）   | 最大值  |
| min（字段）   | 最小值  |
| avg（字段）   | 平均值  |
| sum（字段）   | 求和   |
- 分组：select 字段列表 from 表名 [ where 分组前条件 ] group by 分组字段名 [ having 分组后条件 ];
*==执行顺序：where＞聚合函数＞having==*
### 排序查询
- select 字段列表 from 表名 order by 字段1 排序方式1，字段2 排序方式2，……;
- 排序方式：asc（ascend升序），desc（descend降序）
### 分页查询
- select 字段列表 from 表名 limit 起始索引，查询记录数;
*==起始索引从0开始，起始索引=（查询页码-1）*每页显示记录数==*
## DCL(control控制)
### 用户管理
- 当前主机：localhost
- 通配主机：%
#### 查询用户
- use MySQL;
  select * from user;
#### 创建用户
- create user  '用户名@主机名'  identified by '密码';
#### 修改用户密码
- alter user '用户名@主机名'  identified with mysql_native_password by '新密码';
#### 删除用户
- drop user '用户名@主机名';
### 权限管理

| 权限     | 说明      |
| ------ | ------- |
| all    | 所有权限    |
| select | 查询权限    |
| insert | 插入数据    |
| update | 修改数据    |
| delete | 删除数据    |
| alter  | 修改表     |
| drop   | 删除库/表/图 |
| create | 创建库/表   |
#### 查询权限
- show grants for '用户名@主机名';
#### 授予权限
- grant 权限列表 on 数据库名.表名 to '用户名@主机名';
#### 撤销权限
- revoke 权限列表 on 数据库名.表名 from '用户名@主机名';

# 函数
## 字符串函数

| 函数                       | 功能                 |
| ------------------------ | ------------------ |
| concat（s1，s2，……）         | 字符串拼接              |
| lower（str）               | 转小写                |
| upper（str）               | 转大写                |
| lpad（str，n，pad）          | str左填充字符串pad，直到长度n |
| rpad（str，n，pad）          | 右填充                |
| trim（str）                | 去掉头尾空格             |
| substring（str，start，len） | 返回start开始len长度的子串  |

## 数值函数

| 函数         | 功能          |
| ---------- | ----------- |
| ceil（x）    | 向上取整        |
| floor（x）   | 向下取整        |
| mod（x，y）   | x/y的模       |
| rand（）     | 0~1随机数      |
| round（x，y） | x四舍五入保留y位小数 |

## 日期函数

| 函数                                 | 功能                                 |
| ---------------------------------- | ---------------------------------- |
| curdate（）                          | 当前日期                               |
| curtime（）                          | 当前时间                               |
| now（）                              | 当前日期和时间                            |
| year（date）                         | 指定date年份                           |
| month（date）                        |                                    |
| day（date）                          |                                    |
| date_add（date，interval exper type） | date加上间隔值后的时间（type=day/month/year） |
| datediff（date1，date2）              | date1和date2相差天数                    |

## 流程函数

| 函数                                                             | 功能                                       |
| -------------------------------------------------------------- | ---------------------------------------- |
| if（value，t，f）                                                  | value为true返回t，否则返回f                      |
| ifnull（value1，value2）                                          | value1！=null返回value1，否则返回value2          |
| case when val1 then res1 when val2 then res2……else default end | val1为true返回res1，val2为true返回res2否则default |
# 约束
*==作用于表中字段上，在创建/修改表时添加约束==*

| 约束   | 关键字            | 描述       |
| ---- | -------------- | -------- |
| 非空约束 | not null       |          |
| 唯一约束 | unique         |          |
| 主键约束 | primary key    | 唯一且非空    |
| 默认约束 | default        |          |
| 检查约束 | check          | 保证满足某个条件 |
| 外键约束 | foreign key    | 链接其他表    |
| 自动增长 | auto_increment |          |
## 外键
- 添加外键：create table 表名(

	 [ constraint ]  [ 外键名称 ] foreign key(外键字段名) references 主表(主表列名)  
 )；
alter table 表名 add constraint 外键名称 foreign key(外键字段名) references 主表(主表列表);
- 删除外键：alter table 表名 drop foreign key 外键名称;
- 删除/更新行为：

| 行为          | 说明                   |
| ----------- | -------------------- |
| no action   | 如果父表相应记录有外键，则不许删除/修改 |
| restrict    | 同上                   |
| cascade     | 如有外键，同时删除/修改对应子表记录   |
| set null    | 如有外键，设为null          |
| set default | 如有外键，设为default值      |
alert table 表名 add constraint 外键名称(外键字段) references 主表名(主表名字段) on update 行为1 on delete 行为2;
# 多表查询
## 多表关系
### 一对多（多对一）
如：部门（多位员工）与员工（一个部门）
- 在多的一方（员工）建立外键，指向一（部门）的主键
### 多对多
如：学生与课程
- 建立第三张表，中间表至少包含两个外键，分别关联两张表主键
### 一对一
- 任意一方加入外键关联另一方主键，并且设置外键为UNIQUE
## 多表查询分类
### 连接查询
#### 内连接
查询两张表交集部分(两边数据均不为空)
条件一般为：主键 = 外键
- 隐式：select 字段列表 from 表1，表2 where 条件;
- 显式：select 字段列表 from 表1  [ inner ] join 表2 on 条件;
#### 外连接
（一边数据可以为空）
- 左外连接：select 字段列表 from 表1 left [ outer ] join 表2 on 条件;
- 右外连接：select 字段列表 from 表1 right [ outer ] join 表2 on 条件;
#### 自连接
select 字段列表 from 表1 别名1 join 表1 别名2 on 条件;
### 联合查询
多次查询结果合并起来（查询列数和数据类型需相同）
union all 不去重，union 去重
- select 字段列表 from 表1 ... 
union [ all ] 
select 字段列表 from 表2 ...;
### 子查询
SQL语句中嵌套SELECT语句，称为嵌套查询
 - select * from 表名 where/insert/…… 字段列表 = (select 字段列表 from 表名);
# 事务
把一些操作看做整体，同时成功或同时失败
## 操作
- 开启事务：start transaction
- 提交事务（如果成功）：commit
- 回滚事务（如果失败）：rollback
## 特性
- 原子性：最小操作单位，同时成功/失败
- 一致性：事务结束后数据一致
- 隔离性：不受外界并发操作影响
- 持久性：操作结果永久更改
## 并发事务问题

| 问题    | 描述              |
| ----- | --------------- |
| 脏读    | A读到B未提交的数据      |
| 不可重复读 | A前后两次读取的数据不一样   |
| 幻读    | 查询时未见数据，插入时出现数据 |
## 事务隔离级别

| 隔离级别（从松到严）          | 脏读（是否会出现） | 不可重复读 | 幻读  |
| ------------------- | --------- | ----- | --- |
| read uncommitted    | ✓         | ✓     | ✓   |
| read committed      | ✕         | ✓     | ✓   |
| repeatable read（默认） | ✕         | ✕     | ✓   |
| serializable        | ✕         | ✕     | ✕   |


