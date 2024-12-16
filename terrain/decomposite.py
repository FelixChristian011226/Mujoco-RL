import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import coacd
import trimesh
import os

# 创建窗口
root = tk.Tk()
root.title("COACD Convex Decomposition Tool")

# 设置默认参数
default_params = {
    "threshold": 0.02,
    "max_convex_hull": 10,
    "preprocess_mode": "auto",
    "resolution": 3000,
    "mcts_nodes": 30,
    "mcts_iterations": 200,
    "mcts_max_depth": 4,
    "merge": True,
    "decimate": True,
    "max_ch_vertex": 512,
    "extrude": False,
    "seed": 42
}

# 输入文件选择
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("OBJ Files", "*.obj")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

# 输出文件夹选择
def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_path)

# 执行分解
def run_decomposition():
    input_file = input_file_entry.get()
    output_dir = output_folder_entry.get()

    if not input_file or not output_dir:
        messagebox.showerror("Error", "Please select both input file and output folder.")
        return

    try:
        # 加载模型
        mesh = trimesh.load(input_file, force="mesh")
        mesh = coacd.Mesh(mesh.vertices, mesh.faces)

        # 读取参数
        params = {
            "threshold": float(threshold_entry.get()),
            "max_convex_hull": int(max_convex_hull_entry.get()),
            "preprocess_mode": preprocess_mode_var.get(),
            "resolution": int(resolution_entry.get()),
            "mcts_nodes": int(mcts_nodes_entry.get()),
            "mcts_iterations": int(mcts_iterations_entry.get()),
            "mcts_max_depth": int(mcts_max_depth_entry.get()),
            "merge": merge_var.get(),
            "decimate": decimate_var.get(),
            "max_ch_vertex": int(max_ch_vertex_entry.get()),
            "extrude": extrude_var.get(),
            "seed": int(seed_entry.get())
        }

        # 执行凸分解
        parts = coacd.run_coacd(mesh, **params)

        # 导出分解后的凸包
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i, part in enumerate(parts):
            part_mesh = trimesh.Trimesh(vertices=part[0], faces=part[1])
            part_mesh.export(os.path.join(output_dir, f"part_{i}.obj"))

        messagebox.showinfo("Success", f"Exported {len(parts)} convex parts to {output_dir}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# 创建界面元素
input_file_label = tk.Label(root, text="Input File:")
input_file_label.grid(row=0, column=0, padx=10, pady=5)

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)

input_file_button = tk.Button(root, text="Browse", command=select_input_file)
input_file_button.grid(row=0, column=2, padx=10, pady=5)

output_folder_label = tk.Label(root, text="Output Folder:")
output_folder_label.grid(row=1, column=0, padx=10, pady=5)

output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)

output_folder_button = tk.Button(root, text="Browse", command=select_output_folder)
output_folder_button.grid(row=1, column=2, padx=10, pady=5)

# 参数设置
threshold_label = tk.Label(root, text="Threshold:")
threshold_label.grid(row=2, column=0, padx=10, pady=5)

threshold_entry = tk.Entry(root)
threshold_entry.insert(0, str(default_params["threshold"]))
threshold_entry.grid(row=2, column=1, padx=10, pady=5)

max_convex_hull_label = tk.Label(root, text="Max Convex Hull:")
max_convex_hull_label.grid(row=3, column=0, padx=10, pady=5)

max_convex_hull_entry = tk.Entry(root)
max_convex_hull_entry.insert(0, str(default_params["max_convex_hull"]))
max_convex_hull_entry.grid(row=3, column=1, padx=10, pady=5)

preprocess_mode_label = tk.Label(root, text="Preprocess Mode:")
preprocess_mode_label.grid(row=4, column=0, padx=10, pady=5)

preprocess_mode_var = tk.StringVar(value=default_params["preprocess_mode"])
preprocess_mode_menu = tk.OptionMenu(root, preprocess_mode_var, "auto", "none", "force")
preprocess_mode_menu.grid(row=4, column=1, padx=10, pady=5)

resolution_label = tk.Label(root, text="Resolution:")
resolution_label.grid(row=5, column=0, padx=10, pady=5)

resolution_entry = tk.Entry(root)
resolution_entry.insert(0, str(default_params["resolution"]))
resolution_entry.grid(row=5, column=1, padx=10, pady=5)

mcts_nodes_label = tk.Label(root, text="MCTS Nodes:")
mcts_nodes_label.grid(row=6, column=0, padx=10, pady=5)

mcts_nodes_entry = tk.Entry(root)
mcts_nodes_entry.insert(0, str(default_params["mcts_nodes"]))
mcts_nodes_entry.grid(row=6, column=1, padx=10, pady=5)

mcts_iterations_label = tk.Label(root, text="MCTS Iterations:")
mcts_iterations_label.grid(row=7, column=0, padx=10, pady=5)

mcts_iterations_entry = tk.Entry(root)
mcts_iterations_entry.insert(0, str(default_params["mcts_iterations"]))
mcts_iterations_entry.grid(row=7, column=1, padx=10, pady=5)

mcts_max_depth_label = tk.Label(root, text="MCTS Max Depth:")
mcts_max_depth_label.grid(row=8, column=0, padx=10, pady=5)

mcts_max_depth_entry = tk.Entry(root)
mcts_max_depth_entry.insert(0, str(default_params["mcts_max_depth"]))
mcts_max_depth_entry.grid(row=8, column=1, padx=10, pady=5)

merge_label = tk.Label(root, text="Merge:")
merge_label.grid(row=9, column=0, padx=10, pady=5)

merge_var = tk.BooleanVar(value=default_params["merge"])
merge_checkbox = tk.Checkbutton(root, variable=merge_var)
merge_checkbox.grid(row=9, column=1, padx=10, pady=5)

decimate_label = tk.Label(root, text="Decimate:")
decimate_label.grid(row=10, column=0, padx=10, pady=5)

decimate_var = tk.BooleanVar(value=default_params["decimate"])
decimate_checkbox = tk.Checkbutton(root, variable=decimate_var)
decimate_checkbox.grid(row=10, column=1, padx=10, pady=5)

max_ch_vertex_label = tk.Label(root, text="Max CH Vertex:")
max_ch_vertex_label.grid(row=11, column=0, padx=10, pady=5)

max_ch_vertex_entry = tk.Entry(root)
max_ch_vertex_entry.insert(0, str(default_params["max_ch_vertex"]))
max_ch_vertex_entry.grid(row=11, column=1, padx=10, pady=5)

extrude_label = tk.Label(root, text="Extrude:")
extrude_label.grid(row=12, column=0, padx=10, pady=5)

extrude_var = tk.BooleanVar(value=default_params["extrude"])
extrude_checkbox = tk.Checkbutton(root, variable=extrude_var)
extrude_checkbox.grid(row=12, column=1, padx=10, pady=5)

seed_label = tk.Label(root, text="Seed:")
seed_label.grid(row=13, column=0, padx=10, pady=5)

seed_entry = tk.Entry(root)
seed_entry.insert(0, str(default_params["seed"]))
seed_entry.grid(row=13, column=1, padx=10, pady=5)

# 运行按钮
run_button = tk.Button(root, text="Run Decomposition", command=run_decomposition)
run_button.grid(row=14, column=0, columnspan=3, pady=10)

# 启动主循环
root.mainloop()
