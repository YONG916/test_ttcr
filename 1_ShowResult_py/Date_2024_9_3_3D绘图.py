
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filepath = ("D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin"
            "\\x64\Debug\\3D_builder\\TestScripts\\TestResult\\")
filename = "runtime_TestTertiaryNodes.csv"
df = pd.read_csv(filepath + filename)
# xpos, ypos = df[df.columns[0]], df[df.columns[1]]


# 假设数据是以二维网格方式排列的
x = np.arange(1, 11)  # TertiaryNodes的取值范围
y = np.arange(1, 11)  # SrcRadiusTertiary的取值范围

# 使用np.meshgrid生成二维网格
xpos, ypos = np.meshgrid(x, y)
# TotalTimeSeconds作为z轴的高度值，假设是以100个值排列的（10 x 10）

# 将二维网格展平成一维
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)

# # 设置柱状图的尺寸
dx = dy = 0.5
dz = np.array(df['TotalTimeSeconds'])


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D柱状图
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

# 添加标签和标题
ax.set_ylabel('Tertiary Nodes')
ax.set_xlabel('Src Radius Tertiary')
ax.set_zlabel('Total Time Seconds')
ax.set_title('3D Bar Plot of Total Time Seconds')

plt.show()
z = np.array(df['TotalTimeSeconds']).reshape(10, 10)
# 绘制曲面图

# fig = plt.figure(figsize=(12, 8))
# # 使用np.meshgrid生成二维网格
# xpos1, ypos1 = np.meshgrid(x, y)
# z = np.array(df['TotalTimeSeconds']).reshape(10, 10)
#
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(xpos1, ypos1, z, cmap='viridis')
#
# # 添加标签和标题
# ax.set_xlabel('Tertiary Nodes')
# ax.set_ylabel('Src Radius Tertiary')
# ax.set_zlabel('Total Time Seconds')
# ax.set_title('3D Surface Plot of Total Time Seconds')
#
# plt.show()
print('最大时间与最小时间的差值：', np.max(df['TotalTimeSeconds']) - np.min(df['TotalTimeSeconds']))


# 提取 tertiary nodes = 10 的剖面（第10行）
profile_tn_10 = z[-1, :]  # 最后一行对应 tertiary nodes = 10
src_radius_values = np.arange(1, 11)

plt.figure(figsize=(10, 6))
plt.plot(src_radius_values, profile_tn_10, marker='o')
plt.title('Profile of Total Time Seconds at Tertiary Nodes = 10')
plt.xlabel('Src Radius Tertiary')
plt.ylabel('Total Time Seconds')
plt.grid(True)
plt.show()

# 提取 src radius tertiary = 10 的剖面（第10列）
profile_sr_10 = z[:, -1]  # 最后一列对应 src radius tertiary = 10
tertiary_nodes_values = np.arange(1, 11)

plt.figure(figsize=(10, 6))
plt.plot(tertiary_nodes_values, profile_sr_10, marker='o')
plt.title('Profile of Total Time Seconds at Src Radius Tertiary = 10')
plt.xlabel('Tertiary Nodes')
plt.ylabel('Total Time Seconds')
plt.grid(True)
plt.show()