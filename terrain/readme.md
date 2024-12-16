### 一、文件夹结构说明

- **component** : 通过gen_*.py文件生成的地形组件，如石子、楼梯等。
- **gen_component** : 用于生成地形组件的py文件。
- **hfield** : 高场数据的bin文件，可生成高场地形。
- **mesh** : 引用的stl模型文件。
- **model** : Mujoco可直接调用的地形XML文件。
- **sample_image** : 地形生成工具gen_terrain.py界面展示的示例图。
- **texture** : 纹理图片。



### 二、gen_terrain_gui使用说明

1. 由于我在WSL-Ubuntu上直接安装会报错，需要安装gtk依赖：

   ```bash
   sudo apt-get install libgtk3.0-dev 
   ```

2. 然后安装WxPython：

   ```bash
   pip install -U wxPython
   ```

3. 最后在当前目录直接运行即可：

   ```bash
   python3 gen_terrain.py
   ```

4. 在GUI界面中调整参数，点击生成之后，相应的xml文件会自动生成在component文件夹中。






### 三、gen_component文件说明

*gen_component*文件夹中的py文件是为生成最终地形，将带随机性或规律性的部分拆解出来单独生成，而编写的文件。

**gen_pebble.py** : 在component文件夹中生成随机石头配置的xml文件。参数解释如下：

- num_stones：石头数量
- path_length：路径长度
- path_width：路径宽度

**gen_pit.py** : 在component文件夹生成坑的配置。参数如下：

- num_steps：阶梯数量
- min_radius：底层半径
- step_height：阶梯高度
- horizontal_shift：阶梯水平位移

**gen_stage.py** : 在component文件夹生成台的配置。参数如下：

- num_steps：阶梯数量
- min_radius：顶层半径
- step_height：阶梯高度
- horizontal_shift：阶梯水平位移

**gen_stair.py** : 在component文件夹生成楼梯的配置。参数如下：

- num_steps：台阶数量
- step_width：台阶宽度
- step_height：台阶高度
- step_length：台阶长度
- horizontal_shift：每级台阶偏移量

**gen_trench.py** : 在component文件夹生成沟渠的配置。参数如下：

- length：沟渠的长度
- unit_length：方块的单位长度
- x_scale：x方向的缩放因子
- y_scale：y方向的缩放因子
- z_scale：z方向的缩放因子



### 四、model文件说明

*model*目录下的xml文件是最终形成的各个地形文件，解释如下。

- **mesh_monte.xml**：STL，山峰。
- **hfield_mountains.xml**：通过读入灰度图像，生成高度场，形成崎岖地形。
- **pebbleroad.xml**：读入./component/pebble.xml生成的石子路。
- **pit.xml**：读入./component/pit.xml生成的坑。
- **stage.xml**：读入./component/stage.xml生成的坑。
- **stairs.xml**：读入./component/stair.xml生成的楼梯。
- **trench.xml**：读入./component/trench.xml生成的沟渠。



### 五、注意事项

由于文件引用的是**相对路径**，使用时应当注意工作目录。
- 若要直接使用`gen_component`中的组件，请在`terrain`目录下进行调用。
- 使用`model`中的xml模型时，无须关心组件引用状态，若对当前文件结构无更改，应该可以直接正常运行。

