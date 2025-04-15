import os
import shutil
import coacd
import trimesh
import xml.etree.ElementTree as ET

def run_convex_decomposition(input_folder, output_folder, name=""):
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

    # Create Asset and subfolder
    asset_folder = os.path.join(output_folder, "Asset")
    part_folder = os.path.join(asset_folder, name) if name else asset_folder
    os.makedirs(part_folder, exist_ok=True)

    # Export convex parts
    part_prefix = f"{name}_" if name else ""
    for i, part in enumerate(parts):
        part_mesh = trimesh.Trimesh(vertices=part[0], faces=part[1])
        part_filename = f"{part_prefix}part_{i}.obj"
        part_mesh.export(os.path.join(part_folder, part_filename))

    # Copy texture with prefix
    tex_filename = f"{part_prefix}material_0.png"
    shutil.copy(texture_path, os.path.join(asset_folder, tex_filename))

    return len(parts), part_folder, tex_filename


def create_xml(output_folder, model_name, num_parts, name="", part_folder=None, tex_file="material_0.png"):
    asset_path = "Asset"
    xml_path = os.path.join(output_folder, f"{model_name}.xml")

    name_prefix = f"{name}_" if name else ""
    part_folder_rel = f"{name}/" if name else ""

    # 命名前缀
    tex_name = f"tex_{name}" if name else f"tex_{model_name}"
    mat_name = f"mat_{name}" if name else f"mat_{model_name}"

    root = ET.Element("mujoco")
    asset = ET.SubElement(root, "asset")
    worldbody = ET.SubElement(root, "worldbody")

    # 添加 texture 和 material
    ET.SubElement(asset, "texture", {
        "type": "2d",
        "file": f"{asset_path}/{tex_file}",
        "name": tex_name
    })
    ET.SubElement(asset, "material", {
        "name": mat_name,
        "texture": tex_name
    })

    # 添加所有 mesh（凸包）
    for i in range(num_parts):
        mesh_name = f"{name}_part_{i}" if name else f"{model_name}_part_{i}"
        ET.SubElement(asset, "mesh", {
            "file": f"{asset_path}/{part_folder_rel}{name_prefix}part_{i}.obj",
            "name": mesh_name
        })

    # 添加 visual mesh
    visual_mesh_name = f"{name}_visual" if name else f"{model_name}_visual"
    ET.SubElement(asset, "mesh", {
        "file": f"{asset_path}/{name_prefix}mesh.obj",
        "name": visual_mesh_name,
        "scale": "1 1 1"
    })

    # body 1：physics
    physics_body_name = f"{name}_physics" if name else f"{model_name}_physics"
    physics_body = ET.SubElement(worldbody, "body", {
        "name": physics_body_name,
        "pos": "0 0 0",
        "euler": "0 0 0"
    })
    for i in range(num_parts):
        mesh_name = f"{name}_part_{i}" if name else f"{model_name}_part_{i}"
        ET.SubElement(physics_body, "geom", {
            "type": "mesh",
            "mesh": mesh_name,
            "rgba": "0 0 0 0"
        })

    # body 2：visual
    visual_body_name = f"{name}_visual" if name else f"{model_name}_visual"
    visual_body = ET.SubElement(worldbody, "body", {
        "name": visual_body_name,
        "pos": "0 0 0",
        "euler": "0 0 0"
    })
    ET.SubElement(visual_body, "geom", {
        "type": "mesh",
        "mesh": visual_mesh_name,
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
    parser.add_argument("--name", help="Prefix name for output files", default="")

    args = parser.parse_args()
    model_name = os.path.basename(os.path.abspath(args.input_folder))
    name_prefix = args.name.strip()

    print("Running convex decomposition...")
    num_parts, part_folder, tex_file = run_convex_decomposition(args.input_folder, args.output_folder, name_prefix)

    # Copy mesh with prefix
    mesh_in = os.path.join(args.input_folder, "mesh.obj")
    mesh_out = f"{name_prefix + '_' if name_prefix else ''}mesh.obj"
    shutil.copy(mesh_in, os.path.join(args.output_folder, "Asset", mesh_out))

    print("Creating XML...")
    create_xml(args.output_folder, model_name, num_parts, name_prefix, part_folder, tex_file)

    print("Done.")


if __name__ == "__main__":
    main()
