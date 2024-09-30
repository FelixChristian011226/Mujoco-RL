# CoACD notes

## 安装教程

### (1) 克隆代码：

```
git clone --recurse-submodules https://github.com/SarahWeiii/CoACD.git
```

### (2) 安装依赖：

```
cmake >= 3.24
g++ >= 9, < 12
```

> 在我的Ubuntu22.04中，apt里的cmake包版本是3.22，不能用。用snap成功安装3.30版本。（源码安装好像也行，不过我懒得添加系统变量，就还是用snap安装了。

### (3) 编译

```
cd CoACD \
&& mkdir build \
&& cd build \
```

​	然后编译：

```
cmake .. -DCMAKE_BUILD_TYPE=Release \
&& make main -j
```

> 这里出了很多warning，但是好像不影响使用。

### (4) 使用

```
./main -i PATH_OF_YOUR_MESH -o PATH_OF_OUTPUT
```



## 参数说明

- **-nm/--no-merge** : 禁用合并后处理，默认为false。
- **-c/--max-convex-hull** : 凸包上限，默认-1表示无限制。**仅在启用合并时才**有效。
- **-ex/--extrude** : 沿着重叠面挤出相邻的凸包。
- **-am/--approximate-mode** : 近似形状类型（“ch”表示凸包，“box”表示立方体）。
- **--seed** : 随机种子，默认是random()。

**说明**：

1. 大多数情况下，只需调整`threshold` （0.01~1）即可平衡细节程度和分解成分的数量。值越高，结果越粗，值越低，结果越细。
2. 默认参数是快速版本。可以牺牲运行时间获取更多组件数量，增加`searching depth (-md)` 、 `searching node (-mn)`和`searching iteration (-mi)`可以获得更好的切割策略。