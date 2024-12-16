import wx
from wx import xrc
from wx.lib.agw import floatspin
import coacd
import trimesh
import os


class ConvexDecompositionApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 600))

        self.default_params = {
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

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 输入文件
        self.input_file_label = wx.StaticText(panel, label="Input File:")
        self.input_file_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        input_file_button = wx.Button(panel, label="Browse")
        input_file_button.Bind(wx.EVT_BUTTON, self.on_select_input_file)

        # 输出文件夹
        self.output_folder_label = wx.StaticText(panel, label="Output Folder:")
        self.output_folder_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        output_folder_button = wx.Button(panel, label="Browse")
        output_folder_button.Bind(wx.EVT_BUTTON, self.on_select_output_folder)

        # 参数设置
        self.threshold_label = wx.StaticText(panel, label="Threshold:")
        self.threshold_input = wx.TextCtrl(panel, value=str(self.default_params["threshold"]))

        self.max_convex_hull_label = wx.StaticText(panel, label="Max Convex Hull:")
        self.max_convex_hull_input = wx.TextCtrl(panel, value=str(self.default_params["max_convex_hull"]))

        self.preprocess_mode_label = wx.StaticText(panel, label="Preprocess Mode:")
        self.preprocess_mode_choice = wx.Choice(panel, choices=["auto", "none", "force"])
        self.preprocess_mode_choice.SetSelection(0)

        self.resolution_label = wx.StaticText(panel, label="Resolution:")
        self.resolution_input = wx.TextCtrl(panel, value=str(self.default_params["resolution"]))

        self.mcts_nodes_label = wx.StaticText(panel, label="MCTS Nodes:")
        self.mcts_nodes_input = wx.TextCtrl(panel, value=str(self.default_params["mcts_nodes"]))

        self.mcts_iterations_label = wx.StaticText(panel, label="MCTS Iterations:")
        self.mcts_iterations_input = wx.TextCtrl(panel, value=str(self.default_params["mcts_iterations"]))

        self.mcts_max_depth_label = wx.StaticText(panel, label="MCTS Max Depth:")
        self.mcts_max_depth_input = wx.TextCtrl(panel, value=str(self.default_params["mcts_max_depth"]))

        self.merge_label = wx.StaticText(panel, label="Merge:")
        self.merge_checkbox = wx.CheckBox(panel)
        self.merge_checkbox.SetValue(self.default_params["merge"])

        self.decimate_label = wx.StaticText(panel, label="Decimate:")
        self.decimate_checkbox = wx.CheckBox(panel)
        self.decimate_checkbox.SetValue(self.default_params["decimate"])

        self.max_ch_vertex_label = wx.StaticText(panel, label="Max CH Vertex:")
        self.max_ch_vertex_input = wx.TextCtrl(panel, value=str(self.default_params["max_ch_vertex"]))

        self.extrude_label = wx.StaticText(panel, label="Extrude:")
        self.extrude_checkbox = wx.CheckBox(panel)
        self.extrude_checkbox.SetValue(self.default_params["extrude"])

        self.seed_label = wx.StaticText(panel, label="Seed:")
        self.seed_input = wx.TextCtrl(panel, value=str(self.default_params["seed"]))

        # 运行按钮
        run_button = wx.Button(panel, label="Run Decomposition")
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

        vbox.Add(grid_sizer, 1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(vbox)

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


def main():
    app = wx.App(False)
    frame = ConvexDecompositionApp(None, title="COACD Convex Decomposition Tool")
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
