#coding=utf-8
import wx
import subprocess
import os

class PlaceholderTextCtrl(wx.TextCtrl):
    def __init__(self, parent, default_value):
        super(PlaceholderTextCtrl, self).__init__(parent, -1, default_value, style=wx.TE_LEFT)
        self.default_value = default_value
        self.is_default = True
        
        # 设置初始颜色为灰色
        self.SetForegroundColour(wx.Colour(160, 160, 160))
        
        # 绑定焦点事件
        self.Bind(wx.EVT_SET_FOCUS, self.on_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

    def on_focus(self, event):
        if self.is_default:
            # 清除默认文本并恢复颜色
            self.SetValue("")
            self.SetForegroundColour(wx.Colour(0, 0, 0))  # 正常颜色
            self.is_default = False
        event.Skip()

    def on_kill_focus(self, event):
        if not self.GetValue().strip():  # 如果输入框为空
            # 恢复默认值
            self.SetValue(self.default_value)
            self.SetForegroundColour(wx.Colour(160, 160, 160))  # 灰色
            self.is_default = True
        event.Skip()

class Page1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        # 创建垂直的BoxSizer用于布局
        v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图片到页面顶部
        image_path = "./sample_image/stair.png"
        if os.path.exists(image_path):
            image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 400)  # 调整图片大小
            image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(image))
            v_box_sizer.Add(image_ctrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        else:
            v_box_sizer.Add(wx.StaticText(self, label="Image not found"), proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)


        # 添加输入框和标签，带默认值
        self.num_steps = PlaceholderTextCtrl(self, "6")
        self.step_width = PlaceholderTextCtrl(self, "2.0")
        self.step_height = PlaceholderTextCtrl(self, "0.5")
        self.step_length = PlaceholderTextCtrl(self, "4.0")
        self.horizontal_shift = PlaceholderTextCtrl(self, "1.0")

        v_box_sizer.Add(wx.StaticText(self, label='阶梯数量(num_steps):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.num_steps, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='台阶宽度(step_width):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.step_width, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='台阶高度(step_height):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.step_height, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='台阶长度(step_length):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.step_length, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='台阶水平位移(horizontal_shift):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.horizontal_shift, proportion=0, flag=wx.EXPAND)

        # 添加按钮并绑定事件
        generate_button = wx.Button(self, label="生成XML文件")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        v_box_sizer.Add(generate_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 创建一个透明的面板，覆盖在其他控件之上
        self.transparent_panel = wx.Panel(self, size=self.GetSize())
        self.transparent_panel.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # 设置为透明
        self.transparent_panel.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)


        self.SetSizer(v_box_sizer)

        # 绑定面板的鼠标点击事件
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

    def on_click_blank(self, event):
        self.transparent_panel.SetFocus()

    def on_generate_button(self, event):
        # 获取输入的参数
        num_steps = self.num_steps.GetValue()
        step_width = self.step_width.GetValue()
        step_height = self.step_height.GetValue()
        step_length = self.step_length.GetValue()
        horizontal_shift = self.horizontal_shift.GetValue()

        # 使用subprocess调用外部Python文件
        try:
            subprocess.run([
                "python3", "./gen_component/gen_stair.py",
                num_steps, step_width, step_height, step_length, horizontal_shift
            ], check=True)
            wx.MessageBox('XML file generated successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error occurred: {str(e)}", 'Error', wx.OK | wx.ICON_ERROR)
 
class Page2(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        # 创建垂直的BoxSizer用于布局
        v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图片到页面顶部
        image_path = "./sample_image/pebble.png"
        if os.path.exists(image_path):
            image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 400)  # 调整图片大小
            image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(image))
            v_box_sizer.Add(image_ctrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        else:
            v_box_sizer.Add(wx.StaticText(self, label="Image not found"), proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)


        # 添加输入框和标签，带默认值
        self.num_stones = PlaceholderTextCtrl(self, "100")
        self.path_length = PlaceholderTextCtrl(self, "5.0")
        self.path_width = PlaceholderTextCtrl(self, "1.0")

        v_box_sizer.Add(wx.StaticText(self, label='石子数量(num_stones):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.num_stones, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='石子路长度(path_length):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.path_length, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='石子路宽度(path_width):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.path_width, proportion=0, flag=wx.EXPAND)

        # 添加按钮并绑定事件
        generate_button = wx.Button(self, label="生成XML文件")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        v_box_sizer.Add(generate_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 创建一个透明的面板，覆盖在其他控件之上
        self.transparent_panel = wx.Panel(self, size=self.GetSize())
        self.transparent_panel.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # 设置为透明
        self.transparent_panel.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

        self.SetSizer(v_box_sizer)

        # 绑定面板的鼠标点击事件
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

    def on_click_blank(self, event):
        self.transparent_panel.SetFocus()

    def on_generate_button(self, event):
        # 获取输入的参数
        num_stones = self.num_stones.GetValue()
        path_length = self.path_length.GetValue()
        path_width = self.path_width.GetValue()

        # 使用subprocess调用外部Python文件
        try:
            subprocess.run([
                "python3", "./gen_component/gen_pebble.py",
                num_stones, path_length, path_width
            ], check=True)
            wx.MessageBox('XML file generated successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error occurred: {str(e)}", 'Error', wx.OK | wx.ICON_ERROR)
 
 
class Page3(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        # 创建垂直的BoxSizer用于布局
        v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图片到页面顶部
        image_path = "./sample_image/pit.png"
        if os.path.exists(image_path):
            image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 400)  # 调整图片大小
            image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(image))
            v_box_sizer.Add(image_ctrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        else:
            v_box_sizer.Add(wx.StaticText(self, label="Image not found"), proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)


        # 添加输入框和标签，带默认值
        self.num_steps = PlaceholderTextCtrl(self, "6")
        self.min_radius = PlaceholderTextCtrl(self, "0.2")
        self.step_height = PlaceholderTextCtrl(self, "0.1")
        self.horizontal_shift = PlaceholderTextCtrl(self, "0.2")

        v_box_sizer.Add(wx.StaticText(self, label='阶梯数量(num_steps):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.num_steps, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='底层半径(min_radius):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.min_radius, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='阶梯高度(step_height):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.step_height, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='水平位移(horizontal_shift):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.horizontal_shift, proportion=0, flag=wx.EXPAND)

        # 添加按钮并绑定事件
        generate_button = wx.Button(self, label="生成XML文件")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        v_box_sizer.Add(generate_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 创建一个透明的面板，覆盖在其他控件之上
        self.transparent_panel = wx.Panel(self, size=self.GetSize())
        self.transparent_panel.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # 设置为透明
        self.transparent_panel.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)


        self.SetSizer(v_box_sizer)

        # 绑定面板的鼠标点击事件
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

    def on_click_blank(self, event):
        self.transparent_panel.SetFocus()

    def on_generate_button(self, event):
        # 获取输入的参数
        num_steps = self.num_steps.GetValue()
        min_radius = self.min_radius.GetValue()
        step_height = self.step_height.GetValue()
        horizontal_shift = self.horizontal_shift.GetValue()

        # 使用subprocess调用外部Python文件
        try:
            subprocess.run([
                "python3", "./gen_component/gen_pit.py",
                num_steps, min_radius, step_height, horizontal_shift
            ], check=True)
            wx.MessageBox('XML file generated successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error occurred: {str(e)}", 'Error', wx.OK | wx.ICON_ERROR)


class Page4(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        # 创建垂直的BoxSizer用于布局
        v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图片到页面顶部
        image_path = "./sample_image/stage.png"
        if os.path.exists(image_path):
            image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 400)  # 调整图片大小
            image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(image))
            v_box_sizer.Add(image_ctrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        else:
            v_box_sizer.Add(wx.StaticText(self, label="Image not found"), proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)


        # 添加输入框和标签，带默认值
        self.num_steps = PlaceholderTextCtrl(self, "6")
        self.min_radius = PlaceholderTextCtrl(self, "0.2")
        self.step_height = PlaceholderTextCtrl(self, "0.1")
        self.horizontal_shift = PlaceholderTextCtrl(self, "0.2")

        v_box_sizer.Add(wx.StaticText(self, label='阶梯数量(num_steps):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.num_steps, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='顶层半径(min_radius):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.min_radius, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='阶梯高度(step_height):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.step_height, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='水平位移(horizontal_shift):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.horizontal_shift, proportion=0, flag=wx.EXPAND)

        # 添加按钮并绑定事件
        generate_button = wx.Button(self, label="生成XML文件")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        v_box_sizer.Add(generate_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 创建一个透明的面板，覆盖在其他控件之上
        self.transparent_panel = wx.Panel(self, size=self.GetSize())
        self.transparent_panel.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # 设置为透明
        self.transparent_panel.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)


        self.SetSizer(v_box_sizer)

        # 绑定面板的鼠标点击事件
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

    def on_click_blank(self, event):
        self.transparent_panel.SetFocus()

    def on_generate_button(self, event):
        # 获取输入的参数
        num_steps = self.num_steps.GetValue()
        min_radius = self.min_radius.GetValue()
        step_height = self.step_height.GetValue()
        horizontal_shift = self.horizontal_shift.GetValue()

        # 使用subprocess调用外部Python文件
        try:
            subprocess.run([
                "python3", "./gen_component/gen_stage.py",
                num_steps, min_radius, step_height, horizontal_shift
            ], check=True)
            wx.MessageBox('XML file generated successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error occurred: {str(e)}", 'Error', wx.OK | wx.ICON_ERROR)

class Page5(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        # 创建垂直的BoxSizer用于布局
        v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图片到页面顶部
        image_path = "./sample_image/trench.png"
        if os.path.exists(image_path):
            image = wx.Image(image_path, wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 400)  # 调整图片大小
            image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(image))
            v_box_sizer.Add(image_ctrl, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        else:
            v_box_sizer.Add(wx.StaticText(self, label="Image not found"), proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)


        # 添加输入框和标签，带默认值
        self.length = PlaceholderTextCtrl(self, "5")
        self.unit_length = PlaceholderTextCtrl(self, "0.5")
        self.y_scale = PlaceholderTextCtrl(self, "1.0")
        self.z_scale = PlaceholderTextCtrl(self, "1.0")

        v_box_sizer.Add(wx.StaticText(self, label='沟长度(length):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.length, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='单位长度(unit_length):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.unit_length, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='y轴缩放比(y_scale):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.y_scale, proportion=0, flag=wx.EXPAND)

        v_box_sizer.Add(wx.StaticText(self, label='z轴缩放比(z_scale):'), proportion=0, flag=wx.EXPAND)
        v_box_sizer.Add(self.z_scale, proportion=0, flag=wx.EXPAND)

        # 添加按钮并绑定事件
        generate_button = wx.Button(self, label="生成XML文件")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        v_box_sizer.Add(generate_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 创建一个透明的面板，覆盖在其他控件之上
        self.transparent_panel = wx.Panel(self, size=self.GetSize())
        self.transparent_panel.SetBackgroundColour(wx.Colour(0, 0, 0, 0))  # 设置为透明
        self.transparent_panel.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)


        self.SetSizer(v_box_sizer)

        # 绑定面板的鼠标点击事件
        self.Bind(wx.EVT_LEFT_DOWN, self.on_click_blank)

    def on_click_blank(self, event):
        self.transparent_panel.SetFocus()

    def on_generate_button(self, event):
        # 获取输入的参数
        length = self.length.GetValue()
        unit_length = self.unit_length.GetValue()
        y_scale = self.y_scale.GetValue()
        z_scale = self.z_scale.GetValue()

        # 使用subprocess调用外部Python文件
        try:
            subprocess.run([
                "python3", "./gen_component/gen_trench.py",
                length, unit_length, y_scale, z_scale
            ], check=True)
            wx.MessageBox('XML file generated successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error occurred: {str(e)}", 'Error', wx.OK | wx.ICON_ERROR)
 
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="Mujoco地形构建工具")
    frame.SetSize(1280, 960)
    nb = wx.Notebook(frame)
    nb.AddPage(Page1(nb),"楼梯")
    nb.AddPage(Page2(nb),"石子路")
    nb.AddPage(Page3(nb),"坑")
    nb.AddPage(Page4(nb),"台")
    nb.AddPage(Page5(nb),"沟")
    frame.Show()
    app.MainLoop()