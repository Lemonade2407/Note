```

<div id="app">
	//插值表达式渲染
	<h1>{{message}}</h1>
</div>

<script type="module">
	//引入Vue模块
	import{createApp}from Vue网址
	//创建应用实例
	creatApp({
		data(){
			return{
				//返回的数据
				message:'Hello Vue '
			}
		}
	}).mount('#app')//接管id=app控制权
</script>
```
### 常用指令
- 指令:标签上带有v-前缀的特殊属性

| 指令                    | 作用                    |
| --------------------- | --------------------- |
| v-for                 | 列表渲染，遍历容器的元素或者对象的属性   |
| v-bind                | 为HTML标签绑定属性值，如设置href, |
| v-if/v-else-if/v-else |                       |
| v-show                |                       |
| v-model               |                       |
| v-on                  |                       |
