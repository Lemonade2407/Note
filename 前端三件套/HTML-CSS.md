- 标题标签：
```
<h1>标题一<\h1>
......
<h6>标题六<\h6> 
```
- 超链接标签：
```
<a href="目标地址" target="_self"(默认,原页面打开)/“_blank”(其他页面打开)>
```
- 行内样式
```
<span style="color:gray;"内容>
```
- 内部样式
```
<style>
 span{
  color:gray;
 }
</style>
```
- 外部样式：引用单独的css文件
```
<link rel="stylesheet" href="文件地址">
```
- CSS选择器：选取需要设置样式的标签
```
1.元素选择器
	标签名{}:span{}
2.类选择器
	.class属性值{}:.cls{}
	设置class属性:<span class="cls">
3.id选择器(选择唯一元素)
	#id属性值:#hid{}
	设置id属性:<span id="hid">
```
