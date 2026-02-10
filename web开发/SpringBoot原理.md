# 配置优先级
- .properties>.yml>.yaml
# Bean管理
## 作用域
- singleton（默认）：单例，在容器启动时创建，@Lazy可以延迟到第一次使用时创建
- prototype：非单例
- 指定方法：@Scope("prototype")
## 第三方Bean