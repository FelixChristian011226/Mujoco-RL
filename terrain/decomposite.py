import coacd
import trimesh

input_file = "./convex_model/ditch.obj"

# 加载模型
mesh = trimesh.load(input_file, force="mesh")
mesh = coacd.Mesh(mesh.vertices, mesh.faces)

# 设置自定义的参数
parts = coacd.run_coacd(
    mesh,
    threshold=0.02,  # 更高精度的分解
    max_convex_hull=10,  # 限制最大凸包数量为10
    preprocess_mode="auto",  # 使用自动预处理
    resolution=3000,  # 提高分辨率以增加精度
    mcts_nodes=30,  # 增加搜索树的节点数量
    mcts_iterations=200,  # 增加迭代次数
    mcts_max_depth=4,  # 增加搜索树的最大深度
    merge=True,  # 合并较小的凸包
    decimate=True,  # 启用简化处理
    max_ch_vertex=512,  # 每个凸包的最大顶点数
    extrude=False,  # 禁用凸包拉伸
    seed=42  # 固定随机种子
)

# 导出分解后的凸包
import os

output_dir = "./convex_model/output_parts/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i, part in enumerate(parts):
    part_mesh = trimesh.Trimesh(vertices=part[0], faces=part[1])
    part_mesh.export(os.path.join(output_dir, f"part_{i}.obj"))

print(f"Exported {len(parts)} convex parts to {output_dir}")
