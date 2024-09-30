import argparse

def generate_mesh_xml(model_folder, indent_level, total_count):
    indent = '    ' * indent_level  # 创建缩进
    mesh_lines = []
    body_lines = []

    # 生成mesh部分
    for i in range(total_count):
        mesh_line = f'{indent}<mesh file="../mesh/{model_folder}/convex_{i}.stl" name="convex{i}" />'
        mesh_lines.append(mesh_line)

    # 生成body部分
    body_lines.append(f'{indent}<body name="mesh_{model_folder}" pos="0 0 0" euler="0 0 0">')
    for i in range(total_count):
        body_line = f'{indent}    <geom type="mesh" mesh="convex{i}" material="mat_{model_folder}"/>'
        body_lines.append(body_line)
    body_lines.append(f'{indent}</body>')

    # 将结果写入convex.xml文件
    with open('component/convex.xml', 'w') as f:
        f.write("\n".join(mesh_lines) + "\n\n")
        f.write("\n".join(body_lines) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML mesh and body sections.")
    parser.add_argument("model_folder", type=str, help="Model folder name")
    parser.add_argument("indent_level", type=int, help="Indentation level")
    parser.add_argument("total_count", type=int, help="Total number of models")

    args = parser.parse_args()

    generate_mesh_xml(args.model_folder, args.indent_level, args.total_count)
