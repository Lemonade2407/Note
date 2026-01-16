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
按优先度从低到高排序
1.元素选择器
	标签名{}:span{}
2.类选择器
	.class属性值{}:.cls{}
	设置class属性:<span class="cls">
3.id选择器(选择唯一元素)
	#id属性值:#hid{}
	设置id属性:<span id="hid">
	
1.分组选择器
	选择器1，选择器2{}:h1,h2{}
2.属性选择器
	元素名称[属性]{}:input[type]{}
	元素名称[属性名="值"]{}:input[type="text"]{}
3.后代选择器
	元素1，元素2{}:form,input{}
```
- 插入视频
```
标签:<video>
属性:
	src:视频地址
	controls:显示播放控件(进度条等)
	autoplay:是否自动播放
	width/height:视频高度和宽度
		单位:px(像素)、%(百分比)
```
- 换行
```
<br></br>
```