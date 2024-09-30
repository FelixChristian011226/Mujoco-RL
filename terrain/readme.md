

### 一、文件夹结构说明

- **component** : 通过gen_*.py文件生成的地形组件，如石子、楼梯等。
- **mesh** : 引用的stl模型文件。
- **texture** : 纹理图片。



### 二、py文件说明

py文件是为生成最终地形，将带随机性或规律性的部分拆解出来单独生成，而编写的文件。

**gen_pebble.py** : 在component文件夹中生成随机石头配置的xml文件。参数解释如下：

- num_stones：石头数量。
- path_length：路径长度。
- path_width：路径宽度。

**gen_stair.py** : 在component文件夹生成楼梯的配置。参数如下：

- num_steps：台阶数量。
- step_width：台阶宽度。
- step_height：台阶高度。
- step_length：台阶长度。
- horizontal_shift：每级台阶偏移量。



### 三、xml文件说明

工作目录下的xml文件是最终形成的各个地形文件，解释如下。

- **monte.xml**：STL，山峰。
- **mountains.xml**：通过读入灰度图像，生成高度场，形成崎岖地形。
- **pebbleroad.xml**：读入pebble.xml生成的石子路。
- **stairs.xml**：读入stair.xml生成的楼梯。
- **trench.xml**：STL，沟。

### 四、注意事项

由于文件引用的是**相对路径**，使用时应当注意工作目录。
- 若要使用`gen_component`中的组件，请在`terrain`目录下进行调用。
- 使用`model`中的xml模型时，无须关心组件引用状态，若对当前文件结构无更改，应该可以直接正常运行。


