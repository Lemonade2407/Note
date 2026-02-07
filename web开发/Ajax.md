- 用于网页部分区域刷新
```
1.异步
axios.请求方式(url).then(成功回调函数).catch(失败回调函数)
2.同步
async 函数名(){
let result = await axios.请求方式(url);
}
```