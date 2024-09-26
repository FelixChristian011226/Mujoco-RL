# hfield

>The **hfield** type defines a height field geom. The geom must reference the desired height field asset with the hfield attribute below. The position and orientation of the geom set the position and orientation of the height field. The size of the geom is ignored, and the size parameters of the height field asset are used instead. See the description of the [hfield](https://mujoco.readthedocs.io/en/stable/XMLreference.html#asset-hfield) element. Similar to planes, height field geoms can only be attached to the world body or to static children of the world.

1. 可从PNG的灰度图像加载高场数据。每个像素即为一个高度，黑低白高。

2. 可从bin文件读入，格式如下：

   ```
   (int32)   nrow
   (int32)   ncol
   (float32) data[nrow*ncol]
   ```

3. 高度数据可以在编译时保持未定义。

- 编译器会自动把高度数据归一化到[0,1]
- 高场的位置和方向由geom确定，空间范围由hfield的size字段决定。（与mesh相同）
- 高场视为三棱柱的并集，碰撞时首先确认可能碰撞的棱柱网格，然后通过凸面碰撞器计算。高场和geom的碰撞上限限制为50，超过的则被舍弃。

## 参数

- **name**: 名称，用于引用。如果忽略name，可用不带路径和后缀名的文件名代替引用。
- **content_type**: 目前支持`image/png`和`image/vnd.mujoco.hfield`。
- **file**: 文件名，若后缀为`.png`（不区分大小写），则按图像读入；否则以二进制文件读入。
- **nrow**, **ncol**: 行数和列数。默认值 0 表示将从文件加载数据。
- **elevation**: 高场，自动归一，默认值0。
- **size**: (radius_x、radius_y、elevation_z、base_z)，分别是x、y方向的半径，最大高度，和基础厚度。

## 使用样例

```xml
<mujoco>
    <asset>
      <hfield file="./data/height_field.bin" name="customTerrain" ncol="100" nrow="100" size="50 50 1 0.1"/>
    </asset>
    <worldbody>
      <geom hfield="customTerrain" pos="0 0 0" type="hfield"/>
    </worldbody>
</mujoco>
```

