import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_heightfield(filename):
    # 读取文件中的数据
    data = np.loadtxt(filename)

    # 获取行和列
    rows, cols = data.shape

    # 创建网格坐标
    x = np.linspace(0, cols - 1, cols)
    y = np.linspace(0, rows - 1, rows)
    x, y = np.meshgrid(x, y)

    # 创建一个3D绘图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制表面
    ax.plot_surface(x, y, data, cmap='viridis')

    # 添加标题和标签
    ax.set_title('Height Field Visualization')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Height')

    # 显示图形
    plt.show()

if __name__ == "__main__":
    # 文件名与C++生成的文件保持一致
    visualize_heightfield('./hfield/heightfield.txt')
