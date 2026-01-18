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
- 