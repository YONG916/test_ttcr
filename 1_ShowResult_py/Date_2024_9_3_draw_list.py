import matplotlib.pyplot as plt

# 数据
secondary_nodes = list(range(8))
build_grid_time = [0.7474529, 2.5274399, 5.2374003, 9.2811412, 14.601125, 20.3150644, 42.4137375, 41.4206808]
raytracing_time = [1.7296603, 20.4623533, 93.3722908, 283.2945615, 656.5223637, 1348.4789995, 2456.5347199, 4215.8624974]
total_time = [2.4771132, 22.9897932, 98.6096911, 292.5757027, 671.1234887, 1368.7940594, 2498.9484574, 4257.2831782]

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制每个类别的曲线图
plt.plot(secondary_nodes, total_time, label='Total Time', marker='o')

plt.plot(secondary_nodes, build_grid_time, label='Build Grid Time', marker='o')
plt.plot(secondary_nodes, raytracing_time, label='Raytracing Time', marker='o')

# 添加标题和标签
plt.title('Time Analysis for Different Secondary Nodes')
plt.xlabel('Number of Secondary Nodes')
plt.ylabel('Time (seconds)')

# 显示图例
plt.legend()

# 显示网格线
plt.grid(True)

# 显示图形
plt.show()
