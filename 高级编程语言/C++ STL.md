# Vector
- 动态内存数组
- 头文件`#include <Vector>`
## 声明与初始化
`vector<T> v;`
## 运算
### 插入
- 末端插入：`v.push_back(value);`
- 任意位置：`v.insert(position,value);`
### 访问
- `v[i]或者v.at(i)`
### 求数组大小
- `v.size()`
### 删除
- 末端删除：`v.pop_back();`
- 任意位置：`v.erase(iterator);`
