import pyvista as pv
import matplotlib.pyplot as plt
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\2D_builder\\"

# 文件名列表
filenames = [
    "output\\model2d_rp.vtp",
    "intput\\rcv.vtp",
    "intput\\src.vtp",
]

# 创建一个 Matplotlib 图像
fig, ax = plt.subplots()

# 定义颜色列表，供不同的文件使用
colors = ['r', 'g', 'b']

# 循环读取每个 .vtp 文件并提取坐标数据进行绘制
for idx, filename in enumerate(filenames):
    # 读取 VTP 文件
    mesh = pv.read(filepath + filename)

    # 假设你的 VTP 文件包含点坐标数据
    points = mesh.points

    # 提取 x, y 坐标
    x = points[:, 0]
    z = points[:, 2]

    # 绘制点云数据
    ax.scatter(x, z, color=colors[idx], label=filename)

# 添加图例
ax.legend()

# 设置轴标签和标题
ax.set_xlabel('x')
ax.set_ylabel('Depth (z)')
ax.set_title('Combined VTP Data Plot')
# 反转 y 轴，使深度从 0 到 40
ax.set_ylim(ax.get_ylim()[::-1])
# 显示结果
plt.show()