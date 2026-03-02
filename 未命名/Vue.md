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
# 常用指令
- 指令:标签上带有v-前缀的特殊属性

| 指令                    | 作用                             | 语法                                                              |
| --------------------- | ------------------------------ | --------------------------------------------------------------- |
| v-for                 | 列表渲染，遍历容器的元素或者对象的属性            | `<tr v-for="(item,index) in items":key="item.id">{{item}}</tr>` |
| v-bind                | 为HTML标签绑定属性值，如设置href,css样式     | `v-bind:属性名="属性值"`可略写为`:属性名="属性值"`                              |
| v-if/v-else-if/v-else | 条件为true时渲染，适用不频繁切换             | `v-if="判定条件"`                                                   |
| v-show                | 根据条件展示某元素，切换的是display属性，适用频繁切换 | `v-show="判定条件"`                                                 |
| v-model               | 表单元素双向数据绑定                     | `v-model="绑定元素"`                                                |
| v-on                  | 为标签绑定事件                        | `v-on:事件名="方法名"`可略写为`@属性名="属性值"`                                |
# 生命周期
- 每个生命阶段对应一个钩子函数，到达这个阶段时，会自动触发钩子函数
- 可以通过重构钩子函数完成某些功能：如进入页面时自动执行某些函数
1.beforeCreate
2.create
3.beforeMount
4.mounted
5.beforeUpdate
6.update
7.beforeUnmount
8.unmounted