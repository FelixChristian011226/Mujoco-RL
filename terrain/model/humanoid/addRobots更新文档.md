# addRobots更新文档

## 一、重构

由于原代码中，将生成的mujoco场景文件内容直接输出到终端，为了简化复制过程，首先对原有的函数进行了重构，将输出直接添加到相应的xml文件中。以下是重构前后的相应函数的对应表格：

| 原函数                                                       | 新函数                                                       | 注释 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| void addHead(const char* filename)                           | void setFileToFile(const char* inputfile, const char* outputfile)<br />void addFileToFile(const char* inputfile, const char* outputfile) | 见下 |
| void addActuator(const char* filename, int idx)              | void addActuatorToFile(const char* inputfile, const char* outputfile, int idx) | 无   |
| void addRobot(const char* filename, int i, int j, double tx, double ty, double angle, int idx) | void addRobotToFile(const char* inputfile, const char* outputfile, int i, int j, double tx, double ty, double angle, int idx) | 无   |
| void addRect(double x, double y, double z, double a, double b, double c, double dx, double dy, double dz) | addRectToFile(const char* outputfile, double x, double y, double z, double a, double b, double c, double dx, double dy, double dz) | 无   |
| bool addRectRing(double w, double h, double a, double z, double dx, double dy, double dz) | bool addRectRingToFile(const char* outputfile, double w, double h, double a, double z, double dx, double dy, double dz) | 无   |

注：在addHead的新函数中set和add的区别是：set是覆盖添加，会删除原有内容，而add则是在原内容上追加内容。由于高场数据需要在\<asset\>中引用资源，所以原有的head.txt被拆分为head1.txt和head2.txt，以便在中间加入资源引用。此外，新的head中还添加了mat_pebble的石子纹理。



## 二、重写

为了更好的满足多地形生成的需求，对原有的buildStair和buildGutter函数进行了重写。下面将介绍重写前后的区别：

### (一)、楼梯

```C++
void
buildStair(double offsetx, double offsety, double offsetz,
	double length, double width, double height, 
	double deltaH, int num)
```

![OldStair](https://gitee.com/felix011226/picbed/raw/master/images/stair.JPG)

在旧的楼梯生成中，楼梯的长宽高是固定的，水平和数值偏移量分别由`length*2.1`和`deltaH`决定。这样无法保证最终生成的总长度在`scale`的范围内。于是做了以下改动：

```c++
void addStairToFile(const char* outputfile, double offsetx, double offsety, double offsetz,
	int rotate, double base_z, double deltaH, int num)
```

![NewStair](https://gitee.com/felix011226/picbed/raw/master/images/4c68dbb2fd27a746b28f0a4074799f3a.jpg)

不同于原本的相同形状的台阶的平移，新的构造中将他们的底部设置为一个高度。除此之外，原来的设定中，长宽高的参数实际上是最终生成长度的两倍，因为mujoco中box的size中参数表示边长的一半。在重写后的函数中，参数就是最终实际生成的长度。由于最终要控制地形被控制在`scale*scale`的范围内，这里就没有再对长宽高自定义，而是通过`num`参数计算出每个台阶的长。

新的函数中多了一个`rotate`的输入参数，它的取值为[0,3]，表示楼梯的旋转方向。



#### (二)、沟

```c++
buildGutter(
	double offsetx, double offsety, double offsetz,
	double head, double tail, double extent, double thick,
	double depth, double wid1, double wid2,
	int num)
```

![](https://gitee.com/felix011226/picbed/raw/master/images/a6024503c5a87d401dea6ff558807dbc.jpg)

如图是`gutter`的一个二维截面，其中被截掉的维度即`extent`表示的宽度。在原本的`buildGutter`中，沟的两侧分别由`head`和`tail`控制长度。中间则由每个重复结构的`wid1`和`wid2`控制。如图所示绿色部分即为一个循环结构。

新的函数声明如下：

```C++
void addGutterToFile(const char* outputfile, double offsetx, double offsety, double offsetz,
	double head, double tail, double extent, double thick,
	double depth, int rotate,
	int num)
```

为了控制总长度在`scale`，这里为了保留`head`和`tail`两个参数，除去了`wid1`和`wid2`两个输入。他们的值分别由`head`,`tail`和`num`决定，当头尾和循环次数确定后，单个循环的长度即可计算出来。

同样的，为了避免混淆，这里的参数也是实际长度，而非mujoco中所定义的长度的一半。

`rotate`的取值这里只有0和1，由对称性只需有两个方向即可。



## 三、新增

除了上述三个地形外（台、楼梯、沟），这次新增了两个地形，分别是石子路和高场。

### (一)、石子路

```C++
/**
 * 生成随机石子
 * @param outputfile 输出文件名
 * @param offsetx x方向偏移
 * @param offsety y方向偏移
 * @param offsetz z方向偏移
 * @param num_levels 层数
 * @param deltaH 每层高度
 * @param density 密度，即每层石子的数量
 * @param pebble_scale 石子缩放比例
 */
void addPebbleToFile(const char* outputfile, double offsetx, double offsety, double offsetz,
	int num_levels, double deltaH, int density, double pebble_scale=1.0)
```

参数定义如注释所言。具体实现中，石子的xyz轴半径、坐标以及z轴旋转角度均为随机生成，但最终的z坐标会提高一个z半径，以实现固定在路面上而非嵌入地面的效果。

### (二)、高场

```c++
/**
 * 生成一个二维高度场数据，符合正态分布
 * @param filename 保存的文件名
 * @param radius 高度场的半径细分程度
 * @param stddevX X方向的标准差
 * @param stddevY Y方向的标准差
 * @param meanX X方向的均值
 * @param meanY Y方向的均值
 */
void genNDHeightField(string filename, int radius, float stddevX, float stddevY, float meanX=0, float meanY=0)
```

该函数生成高场数据文件，存储在`./hfield/heightfield_x.bin`中。（若没有该文件夹，需要先创建，否则生成不了）。

高场的生成选择服从正态分布的运算方式。值得注意的是`radius`并非一个决定尺寸的参数，而是决定细分程度的参数。因为高场最终的尺寸由在`<asset>`里引用的`size`参数决定。这里的`radius`决定了生成的数据的多少，最终`.bin`文件里存储的数据是`2*radius+1`行、`2*radius+1`列的。

为了将高场相关的数据写入`xml`文件，新增了两个函数：

```C++
void addHfieldAssetToFile(string filename, string hfieldname,int index, double radius_x, double radius_y, double elevation_z, double base_z)
void addHeightFieldToFile(string filename, int i, int j, string hfieldname, int index)
```

其中`addHfieldAssetToFile`函数是在`<asset>`中添加相应的文件引入，`radius_x`和`radius_y`与mujoco中一致，表示两个方向上的`size`，`elevation_z`是高度的比例，值越大越抖，`base_z`是基础高度。

`addHeightFieldToFile`则是在`<worldbody>`中添加高场。`index`与上一个函数中的`index`应保持一致。



## 四、主函数实现

在主函数中，对每个区块，会生成一个随机数来确定其地形。对于每个地形都会生成相应的随机数，来区分同种地形。其随机参数如下：

| 类型                 | 参数                                                         |
| -------------------- | ------------------------------------------------------------ |
| **台 stand**         | **angle**: `double`, 确定台是向上凸还是向下凹                |
| **楼梯 stair**       | **stair_rotate**: `int`, 取值0~3，决定楼梯旋转方向<br />**stair_deltaH**: `double`, 取值0.03~0.06，决定楼梯层级间高度差<br />**stair_num**: `int`, 取值10~20，决定楼梯级数 |
| **沟 gutter**        | **gutter_head**: `double`, 取值0.1~0.5，决定沟头长度<br />**gutter_tail**: `double`, 取值0.1~0.5，决定沟尾长度<br />**gutter_num**: `int`, 取值6~12，决定沟的循环次数<br />**gutter_depth**: `double`, 取值0.1~0.2，决定沟深度<br />**gutter_rotate**: `int`, 取值0~1，决定沟旋转方向（横竖） |
| **石子路 pebble**    | **pebble_level**: `int`, 取值2~4，决定石子的层数<br />**pebble_density**: `int`, 取值100~200，决定每层石子数量<br />**pebble_scale**: `double`, 取值1.0~2.0，决定石子的缩放比例 |
| **高场 heightfield** | **height**: `double`, 取值1.0~2.0, 决定高场的高度比例（该参数在`<asset>`中定义） |



