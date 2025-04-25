1. 文件结构介绍
.
├── models              存放训练结果
├── tensorboard         存放训练数据
├── unitree_go1         存放go1机器人模型，以及场景文件
├── decomposite.py      凸分解及导入xml工具
├── go1_mujoco_env.py   训练所定义的go1的mujoco环境
├── train_go1.py        训练及测试代码

2. 使用说明

2.1 train_go1.py说明
该文件为带场景的go1机器人的训练以及测试的文件。
通过以下代码安装前置：
pip install gymnasium[mujoco]
pip install stable_baselines3

如想通过此文件进行go1机器人的训练，请取消main函数里以下行的注释：
model = train(total_timesteps=1000000, model_save_path="./models/go1_room_100w", log_save_path="tensorboard/go1_room_100w")
并设置相应的timestep，modelpath和logpath。然后在终端执行：
python train_go1.py

如想对训练模型进行测试，请在main函数取消该行注释：
test("./models/go1_room_100w", num_steps=1000)
并将第一个参数更改为自己的模型地址，然后在终端执行以下代码：
python train_go1.py

如想对模型进行评估，则取消main函数该行注释：
evaluate(model, num_episodes=5)
然后执行：
python train_go1.py

2.2 decomposite.py说明
该文件为带GUI界面的CoACD凸分解及xml文件导入的整合工具。
通过以下代码安装前置：
pip install wxPython
pip install coacd
pip install trimesh

然后在终端启用该程序：
python decomposite.py

文件有两个页面：Convex Decomposition和XML Insertion
分别执行凸分解和文件导入流程。
凸分解流程：
(1).点击Input File输入框右侧的Browse，选择原始的obj文件。
(2).点击Output Folder输入框右侧的Browse，选择输出文件夹。
(3).根据需求更改其余CoACD所需参数。
(4).点击Run Decomposition按钮执行凸分解。
XML导入流程：
(1).点击Input Folder输入框下方的Browse，选择凸分解模型文件夹。
(2).点击XML File输入框下方的Browse，选择需要导入模型的XML场景文件。
(3).根据需求更改其余模型参数，如位置、旋转角度、缩放比。
(4).点击Insert to XML按钮执行插入。





