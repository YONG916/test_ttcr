import pyvista as pv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# region S0. Predefine some variables
file_root = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\2D_builder\\"
filepath_input = file_root + "input\\"
filepath_output = file_root + "output\\"


# 文件名列表
slowness_filenames = 'model2d.slo'
filenames = [
    "model2d_rp.vtp",
]

file_src_rcv = [
    "src1.dat",
    "rcv.dat"
]

# 使用 GridSpec 创建一个两行一列的布局
fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.1)

# 创建两个子图
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# 定义颜色列表，供不同的文件使用
colors = ['r', 'g', 'b']

# region S1. 处理slowness 文件
# 打开并读取文本文件内容
with open(filepath_input + slowness_filenames, 'r', encoding='utf-8') as file:
    data = file.readlines()  # 使用 readlines() 方法逐行读取文件

# 去除每行的换行符，并将字符串转换为浮点数
try:
    data = [list(map(float, line.strip().split())) for line in data]
except ValueError as e:
    print(f"数据转换错误: {e}")

# 将数据转换为NumPy数组
data = np.array(data)

with open(filepath_input + 'model2d.grd', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 解析数据
number_of_cells = list(map(int, lines[0].split()[:3]))  # 读取网格单元数量
size_of_cells = list(map(float, lines[1].split()[:3]))  # 读取单元格大小
origin_of_grid = list(map(float, lines[2].split()[:3]))  # 读取网格的原点

# 处理数组维度
if number_of_cells[1] == 0:
    data = np.reshape(data, (number_of_cells[0], number_of_cells[2])).T
else:
    data = np.reshape(data, number_of_cells).T

# 在第一个子图中绘制数据
im = ax1.imshow(data, cmap="gray", aspect='auto')
im2 = ax2.imshow(data, cmap="gray", aspect='auto')


# 添加颜色条到第一个子图
fig.colorbar(im, ax=ax1, label='Slowness')
fig.colorbar(im2, ax=ax2, label='Slowness')

# 设置第一个子图的轴标签和标题
ax1.set_title('Slowness (' + slowness_filenames +')')
ax1.set_xlabel('X Coordinate')
ax1.set_ylabel('Depth (Z Coordinate)')

# 获取第一个子图的坐标轴范围
xlim = ax1.get_xlim()
ylim = ax1.get_ylim()
# endregion

# region S2. 处理 vtp 文件
# 循环读取每个 .vtp 文件并提取坐标数据进行绘制在第二个子图

for idx, filename in enumerate(filenames):
    # 读取 VTP 文件
    mesh = pv.read(filepath_output + filename)

    # 假设你的 VTP 文件包含点坐标数据
    points = mesh.points

    # 提取 x, z 坐标
    x = points[:, 0]
    z = points[:, 2]

    ax2.scatter(x, z, color=colors[idx], label=filename, alpha=0.6, s=10)


# 读取src 和 rcv
# 创建两个空列表用于存储 x 和 z 坐标
colors = ['g', 'b']
x_coords = []
z_coords = []
for idx, filename in enumerate(file_src_rcv):
    # 打开并读取文本文件内容
    with open(filepath_input + filename, 'r', encoding='utf-8') as file:
        data = file.readlines()  # 使用 readlines() 方法逐行读取文件

        # 只取第二行之后的内容
        data = data[1:]  # 跳过第一行

        # 对每一行进行处理
        for line in data:
            if line.strip():  # 确保不处理空行
                values = line.split()  # 按空格或其他空白字符分割
                x_coord = float(values[0])  # 第一列是 x 坐标
                z_coord = float(values[1])  # 第二列是 z 坐标

                # 将 x 和 z 坐标分别添加到对应的列表中
                x_coords.append(x_coord)
                z_coords.append(z_coord)

    ax2.scatter(x_coords, z_coords, color=colors[idx], label=filename, alpha=0.6, s=40)
    x_coords, z_coords = [], []

# 添加图例到第二个子图
ax2.legend()

# 设置第二个子图的轴标签和标题
ax2.set_xlabel('X Coordinate')
ax2.set_ylabel('Depth (Z Coordinate)')


# 将第二个子图的坐标轴范围设置为与第一个子图相同
ax2.set_xlim(xlim)
ylim = (ylim[0], ylim[1]  - 1)
ax2.set_ylim(ylim)  # 反转 y 轴，使深度从 0 到 40

# 显示组合图像
plt.show()
#endregion
