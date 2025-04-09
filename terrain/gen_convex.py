import os
import shutil
import coacd
import trimesh
import xml.etree.ElementTree as ET

def run_convex_decomposition(input_folder, output_folder):
    mesh_path = os.path.join(input_folder, "poisson_mesh.ply")
    texture_path = os.path.join(input_folder, "material_0.png")

    if not os.path.exists(mesh_path) or not os.path.exists(texture_path):
        raise FileNotFoundError("Missing required files: poisson_mesh.ply or material_0.png")

    mesh = trimesh.load(mesh_path, force="mesh")
    mesh = coacd.Mesh(mesh.vertices, mesh.faces)

    params = {
        "threshold": 0.05,
        "max_convex_hull": -1,
        "preprocess_mode": "auto",
        "resolution": 2000,
        "mcts_nodes": 20,
        "mcts_iterations": 150,
        "mcts_max_depth": 3,
        "merge": True,
        "decimate": True,
        "max_ch_vertex": 512,
        "extrude": False,
        "seed": 42
    }

    parts = coacd.run_coacd(mesh, **params)

    # Create Asset folder
    asset_folder = os.path.join(output_folder, "Asset")
    os.makedirs(asset_folder, exist_ok=True)

    # Export convex parts
    for i, part in enumerate(parts):
        part_mesh = trimesh.Trimesh(vertices=part[0], faces=part[1])
        part_mesh.export(os.path.join(asset_folder, f"part_{i}.obj"))

    # Copy texture
    shutil.copy(texture_path, os.path.join(asset_folder, "material_0.png"))

    return len(parts)

def create_xml(output_folder, model_name, num_parts):
    asset_path = "Asset"
    xml_path = os.path.join(output_folder, f"{model_name}.xml")

    root = ET.Element("mujoco")
    asset = ET.SubElement(root, "asset")
    worldbody = ET.SubElement(root, "worldbody")

    # 添加 texture 和 material
    tex_name = f"tex_{model_name}"
    mat_name = f"mat_{model_name}"
    ET.SubElement(asset, "texture", {
        "type": "2d",
        "file": f"{asset_path}/material_0.png",
        "name": tex_name
    })
    ET.SubElement(asset, "material", {
        "name": mat_name,
        "texture": tex_name
    })

    # 添加所有 mesh
    for i in range(num_parts):
        ET.SubElement(asset, "mesh", {
            "file": f"{asset_path}/part_{i}.obj",
            "name": f"{model_name}_part_{i}"
        })

    ET.SubElement(asset, "mesh", {
        "file": f"{asset_path}/mesh.obj",
        "name": f"{model_name}_visual",
        "scale": "1 1 1"
    })

    # body 1：用于物理模拟（透明凸包）
    physics_body = ET.SubElement(worldbody, "body", {
        "name": f"{model_name}_physics",
        "pos": "0 0 0",
        "euler": "0 0 0"
    })

    for i in range(num_parts):
        ET.SubElement(physics_body, "geom", {
            "type": "mesh",
            "mesh": f"{model_name}_part_{i}",
            "rgba": "0 0 0 0"
        })

    # body 2：可视化（仅显示）
    visual_body = ET.SubElement(worldbody, "body", {
        "name": f"{model_name}_visual",
        "pos": "0 0 0",
        "euler": "0 0 0"
    })

    ET.SubElement(visual_body, "geom", {
        "type": "mesh",
        "mesh": f"{model_name}_visual",
        "material": mat_name,
        "contype": "0",
        "conaffinity": "0"
    })

    indent_xml(root)
    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"XML saved to {xml_path}")


def indent_xml(elem, level=0):
    indent = "\n" + "    " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "    "
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process Nerfstudio mesh for MuJoCo.")
    parser.add_argument("input_folder", help="Folder containing mesh.obj, poisson_mesh.ply, material_0.mtl, material_0.png")
    parser.add_argument("output_folder", help="Output folder for Asset and XML")

    args = parser.parse_args()
    model_name = os.path.basename(os.path.abspath(args.input_folder))

    print("Running convex decomposition...")
    num_parts = run_convex_decomposition(args.input_folder, args.output_folder)

    print("Copying original mesh...")
    shutil.copy(os.path.join(args.input_folder, "mesh.obj"), os.path.join(args.output_folder, "Asset/mesh.obj"))

    print("Creating XML...")
    create_xml(args.output_folder, model_name, num_parts)

    print("Done.")

if __name__ == "__main__":
    main()
