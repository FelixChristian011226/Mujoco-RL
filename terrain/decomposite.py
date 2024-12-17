import wx
from wx import xrc
import coacd
import trimesh
import os
import xml.etree.ElementTree as ET

class ConvexDecompositionPage(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.default_params = {
            "threshold": 0.05,
            "max_convex_hull": -1,
            "preprocess_mode": "auto",
            "resolution": 2000,
            "mcts_nodes": 20,
            "mcts_iterations": 150,
            "mcts_max_depth": 3,
            "pca": False,
            "merge": True,
            "decimate": True,
            "max_ch_vertex": 512,
            "extrude": False,
            "seed": 42
        }
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入文件
        self.input_file_label = wx.StaticText(self, label="Input File:")
        self.input_file_text = wx.TextCtrl(self, style=wx.TE_READONLY)
        input_file_button = wx.Button(self, label="Browse")
        input_file_button.Bind(wx.EVT_BUTTON, self.on_select_input_file)

        # 输出文件夹
        self.output_folder_label = wx.StaticText(self, label="Output Folder:")
        self.output_folder_text = wx.TextCtrl(self, style=wx.TE_READONLY)
        output_folder_button = wx.Button(self, label="Browse")
        output_folder_button.Bind(wx.EVT_BUTTON, self.on_select_output_folder)

        # 参数设置
        self.threshold_label = wx.StaticText(self, label="Threshold:")
        self.threshold_input = wx.TextCtrl(self, value=str(self.default_params["threshold"]))

        self.max_convex_hull_label = wx.StaticText(self, label="Max Convex Hull:")
        self.max_convex_hull_input = wx.TextCtrl(self, value=str(self.default_params["max_convex_hull"]))

        self.preprocess_mode_label = wx.StaticText(self, label="Preprocess Mode:")
        self.preprocess_mode_choice = wx.Choice(self, choices=["auto", "none", "force"])
        self.preprocess_mode_choice.SetSelection(0)

        self.resolution_label = wx.StaticText(self, label="Resolution:")
        self.resolution_input = wx.TextCtrl(self, value=str(self.default_params["resolution"]))

        self.mcts_nodes_label = wx.StaticText(self, label="MCTS Nodes:")
        self.mcts_nodes_input = wx.TextCtrl(self, value=str(self.default_params["mcts_nodes"]))

        self.mcts_iterations_label = wx.StaticText(self, label="MCTS Iterations:")
        self.mcts_iterations_input = wx.TextCtrl(self, value=str(self.default_params["mcts_iterations"]))

        self.mcts_max_depth_label = wx.StaticText(self, label="MCTS Max Depth:")
        self.mcts_max_depth_input = wx.TextCtrl(self, value=str(self.default_params["mcts_max_depth"]))

        self.merge_label = wx.StaticText(self, label="Merge:")
        self.merge_checkbox = wx.CheckBox(self)
        self.merge_checkbox.SetValue(self.default_params["merge"])

        self.decimate_label = wx.StaticText(self, label="Decimate:")
        self.decimate_checkbox = wx.CheckBox(self)
        self.decimate_checkbox.SetValue(self.default_params["decimate"])

        self.max_ch_vertex_label = wx.StaticText(self, label="Max CH Vertex:")
        self.max_ch_vertex_input = wx.TextCtrl(self, value=str(self.default_params["max_ch_vertex"]))

        self.extrude_label = wx.StaticText(self, label="Extrude:")
        self.extrude_checkbox = wx.CheckBox(self)
        self.extrude_checkbox.SetValue(self.default_params["extrude"])

        self.seed_label = wx.StaticText(self, label="Seed:")
        self.seed_input = wx.TextCtrl(self, value=str(self.default_params["seed"]))

        # 运行按钮
        run_button = wx.Button(self, label="Run Decomposition")
        run_button.Bind(wx.EVT_BUTTON, self.on_run_decomposition)

        # Layout
        grid_sizer = wx.GridBagSizer(vgap=5, hgap=5)
        grid_sizer.Add(self.input_file_label, pos=(0, 0), flag=wx.EXPAND)
        grid_sizer.Add(self.input_file_text, pos=(0, 1), span=(1, 2), flag=wx.EXPAND)
        grid_sizer.Add(input_file_button, pos=(0, 3))

        grid_sizer.Add(self.output_folder_label, pos=(1, 0), flag=wx.EXPAND)
        grid_sizer.Add(self.output_folder_text, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)
        grid_sizer.Add(output_folder_button, pos=(1, 3))

        grid_sizer.Add(self.threshold_label, pos=(2, 0))
        grid_sizer.Add(self.threshold_input, pos=(2, 1))

        grid_sizer.Add(self.max_convex_hull_label, pos=(3, 0))
        grid_sizer.Add(self.max_convex_hull_input, pos=(3, 1))

        grid_sizer.Add(self.preprocess_mode_label, pos=(4, 0))
        grid_sizer.Add(self.preprocess_mode_choice, pos=(4, 1))

        grid_sizer.Add(self.resolution_label, pos=(5, 0))
        grid_sizer.Add(self.resolution_input, pos=(5, 1))

        grid_sizer.Add(self.mcts_nodes_label, pos=(6, 0))
        grid_sizer.Add(self.mcts_nodes_input, pos=(6, 1))

        grid_sizer.Add(self.mcts_iterations_label, pos=(7, 0))
        grid_sizer.Add(self.mcts_iterations_input, pos=(7, 1))

        grid_sizer.Add(self.mcts_max_depth_label, pos=(8, 0))
        grid_sizer.Add(self.mcts_max_depth_input, pos=(8, 1))

        grid_sizer.Add(self.merge_label, pos=(9, 0))
        grid_sizer.Add(self.merge_checkbox, pos=(9, 1))

        grid_sizer.Add(self.decimate_label, pos=(10, 0))
        grid_sizer.Add(self.decimate_checkbox, pos=(10, 1))

        grid_sizer.Add(self.max_ch_vertex_label, pos=(11, 0))
        grid_sizer.Add(self.max_ch_vertex_input, pos=(11, 1))

        grid_sizer.Add(self.extrude_label, pos=(12, 0))
        grid_sizer.Add(self.extrude_checkbox, pos=(12, 1))

        grid_sizer.Add(self.seed_label, pos=(13, 0))
        grid_sizer.Add(self.seed_input, pos=(13, 1))

        grid_sizer.Add(run_button, pos=(14, 0), span=(1, 4), flag=wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(grid_sizer, 1, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(vbox)

    def on_select_input_file(self, event):
        file_dialog = wx.FileDialog(self, "Choose an OBJ file", wildcard="OBJ files (*.obj)|*.obj", style=wx.FD_OPEN)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.input_file_text.SetValue(file_dialog.GetPath())
        file_dialog.Destroy()

    def on_select_output_folder(self, event):
        folder_dialog = wx.DirDialog(self, "Choose output folder", style=wx.DD_DEFAULT_STYLE)
        if folder_dialog.ShowModal() == wx.ID_OK:
            self.output_folder_text.SetValue(folder_dialog.GetPath())
        folder_dialog.Destroy()

    def on_run_decomposition(self, event):
        input_file = self.input_file_text.GetValue()
        output_folder = self.output_folder_text.GetValue()

        if not input_file or not output_folder:
            wx.MessageBox("Please select both input file and output folder.", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            mesh = trimesh.load(input_file, force="mesh")
            mesh = coacd.Mesh(mesh.vertices, mesh.faces)

            params = {
                "threshold": float(self.threshold_input.GetValue()),
                "max_convex_hull": int(self.max_convex_hull_input.GetValue()),
                "preprocess_mode": self.preprocess_mode_choice.GetStringSelection(),
                "resolution": int(self.resolution_input.GetValue()),
                "mcts_nodes": int(self.mcts_nodes_input.GetValue()),
                "mcts_iterations": int(self.mcts_iterations_input.GetValue()),
                "mcts_max_depth": int(self.mcts_max_depth_input.GetValue()),
                "merge": self.merge_checkbox.GetValue(),
                "decimate": self.decimate_checkbox.GetValue(),
                "max_ch_vertex": int(self.max_ch_vertex_input.GetValue()),
                "extrude": self.extrude_checkbox.GetValue(),
                "seed": int(self.seed_input.GetValue())
            }

            parts = coacd.run_coacd(mesh, **params)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for i, part in enumerate(parts):
                part_mesh = trimesh.Trimesh(vertices=part[0], faces=part[1])
                part_mesh.export(os.path.join(output_folder, f"part_{i}.obj"))

            wx.MessageBox(f"Exported {len(parts)} convex parts to {output_folder}", "Success", wx.OK | wx.ICON_INFORMATION)

        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


import os
import xml.etree.ElementTree as ET
import wx

class XMLInsertionPage(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入文件夹选择
        self.input_folder_label = wx.StaticText(self, label="Input Folder:")
        self.input_folder_text = wx.TextCtrl(self, style=wx.TE_READONLY)
        input_folder_button = wx.Button(self, label="Browse")
        input_folder_button.Bind(wx.EVT_BUTTON, self.on_select_input_folder)

        # 输入XML文件选择
        self.xml_file_label = wx.StaticText(self, label="XML File:")
        self.xml_file_text = wx.TextCtrl(self, style=wx.TE_READONLY)
        xml_file_button = wx.Button(self, label="Browse")
        xml_file_button.Bind(wx.EVT_BUTTON, self.on_select_xml_file)

        # pos 输入框
        self.pos_label = wx.StaticText(self, label="Position (pos):")
        self.pos_text = wx.TextCtrl(self, value="0 0 0")
        
        # euler 输入框
        self.euler_label = wx.StaticText(self, label="Euler (euler):")
        self.euler_text = wx.TextCtrl(self, value="0 0 0")

        # scale 输入框
        self.scale_label = wx.StaticText(self, label="Scale (scale):")
        self.scale_text = wx.TextCtrl(self, value="1 1 1")

        # 执行按钮
        execute_button = wx.Button(self, label="Insert to XML")
        execute_button.Bind(wx.EVT_BUTTON, self.on_insert_to_xml)

        # Layout
        vbox.Add(self.input_folder_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.input_folder_text, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(input_folder_button, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add(self.xml_file_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.xml_file_text, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(xml_file_button, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add(self.pos_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.pos_text, 0, wx.EXPAND | wx.ALL, 5)
        
        vbox.Add(self.euler_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.euler_text, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add(self.scale_label, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.scale_text, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add(execute_button, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbox)

    def on_select_input_folder(self, event):
        folder_dialog = wx.DirDialog(self, "Choose Input Folder", style=wx.DD_DEFAULT_STYLE)
        if folder_dialog.ShowModal() == wx.ID_OK:
            self.input_folder_text.SetValue(folder_dialog.GetPath())
        folder_dialog.Destroy()

    def on_select_xml_file(self, event):
        file_dialog = wx.FileDialog(self, "Choose XML File", wildcard="XML files (*.xml)|*.xml", style=wx.FD_OPEN)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.xml_file_text.SetValue(file_dialog.GetPath())
        file_dialog.Destroy()

    def on_insert_to_xml(self, event):
        input_folder = self.input_folder_text.GetValue()
        xml_file = self.xml_file_text.GetValue()
        pos = self.pos_text.GetValue().split()
        euler = self.euler_text.GetValue().split()
        scale = self.scale_text.GetValue().split()

        if len(pos) != 3 or len(euler) != 3 or len(scale) != 3:
            wx.MessageBox("Please enter valid values for pos, euler, and scale (3 values each).", "Error", wx.OK | wx.ICON_ERROR)
            return

        pos = ' '.join(pos)
        euler = ' '.join(euler)
        scale = ' '.join(scale)

        if not input_folder or not xml_file:
            wx.MessageBox("Please select both input folder and XML file.", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            files = [f for f in os.listdir(input_folder) if f.endswith(".obj")]
            files.sort()
            model_folder = os.path.basename(input_folder)
            self.insert_to_xml(xml_file, input_folder, model_folder, files, pos, euler, scale)
            wx.MessageBox("Insertion completed successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

    def insert_to_xml(self, xml_file, input_folder, model_folder, obj_files, pos, euler, scale):
        # 读取XML文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 定义命名空间，如果你的XML中有namespace需要在这里定义，例如：{"mujoco": "http://www.mujoco.org"}
        namespaces = {}

        # 定位 <asset> 和 <worldbody> 标签
        asset = root.find("asset", namespaces)
        worldbody = root.find("worldbody", namespaces)

        if asset is None or worldbody is None:
            raise ValueError("XML file does not contain <asset> or <worldbody> tags.")

        # 计算相对路径
        base_path = os.path.dirname(xml_file)
        relative_folder_path = os.path.relpath(input_folder, base_path)

        # 插入 Material
        material = ET.Element("material")
        material.set("name", f"mat_{model_folder}")
        material.set("rgba", "0.8 0.8 0.8 1")
        asset.insert(0, material)  # 插入到<asset>标签前

        # 插入到 <asset> 中
        for i, file_name in enumerate(obj_files):
            mesh_line = ET.SubElement(asset, "mesh")
            mesh_line.set("file", f"{relative_folder_path}/{file_name}")
            mesh_line.set("name", f"{model_folder}_{i}")
            mesh_line.set("scale", scale)

        # 插入到 <worldbody> 中
        body = ET.SubElement(worldbody, "body")
        body.set("name", f"mesh_{model_folder}")
        body.set("pos", pos)
        body.set("euler", euler)

        for i in range(len(obj_files)):
            geom = ET.SubElement(body, "geom")
            geom.set("type", "mesh")
            geom.set("mesh", f"{model_folder}_{i}")
            geom.set("material", f"mat_{model_folder}")

        # 格式化输出
        self.indent_xml(root)

        # 保存修改后的XML文件
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    def indent_xml(self, elem, level=0):
        """对XML元素进行缩进和格式化"""
        indent = "\n" + "    " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "    "
            for child in elem:
                self.indent_xml(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="COACD Convex Decomposition Tool", size=(1000, 800))
        notebook = wx.Notebook(self)

        # Add pages to the notebook
        convex_page = ConvexDecompositionPage(notebook)
        insert_page = XMLInsertionPage(notebook)

        notebook.AddPage(convex_page, "Convex Decomposition")
        notebook.AddPage(insert_page, "XML Insertion")

        self.Show()


def main():
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()


if __name__ == "__main__":
    main()
