# mujoco notes

## Collision

[Computation - MuJoCo Documentation](https://mujoco.readthedocs.io/en/stable/computation/index.html#collision)

> We have chosen to limit collision detection to *convex* geoms. All primitive types are convex. Height fields are not convex but internally they are treated as unions of triangular prisms (using custom collision pruning beyond the filters described above). Meshes specified by the user can be non-convex, and are rendered as such. For collision purposes however they are replaced with their convex hulls.

- 碰撞检测限制在*凸*几何体
- 所有原始类型都是凸的
- 高度字段不是凸的，但在内部它们被视为三棱柱的并集
- 网格可以是非凸的，并且如此渲染。然而，出于碰撞目的，它们被替换为凸包

> In order to model a non-convex object other than a height field, the user must decompose it into a union of convex geoms (which can be primitive shapes or meshes) and attach them to the same body. Open tools like the [CoACD library](https://github.com/SarahWeiii/CoACD) can be used outside MuJoCo to automate this process. Finally, all built-in collision functions can be replaced with custom callbacks. This can be used to incorporate a general-purpose “triangle soup” collision detector for example. However we do not recommend such an approach. Pre-processing the geometry and representing it as a union of convex geoms takes some work, but it pays off at runtime and yields both faster and more stable simulation.
>
> 为了对高度场以外的非凸对象进行建模，用户必须将其分解为凸几何体（可以是原始形状或网格）的并集并将它们附加到同一实体。可以在 MuJoCo 外部使用[CoACD 库](https://github.com/SarahWeiii/CoACD)等开放工具来自动化此过程。最后，所有内置碰撞函数都可以替换为自定义回调。例如，这可用于合并通用“三角汤”碰撞检测器。但是我们不推荐这种方法。预处理几何体并将其表示为凸几何体的联合需要一些工作，但它在运行时得到回报，并产生更快、更稳定的模拟。

