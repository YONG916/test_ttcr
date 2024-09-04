import numpy as np

filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\3D_builder\\input\\"
# 生成 20 个节点的 x 和 y 数据
x_values = np.arange(5, 50, 10)
y_values = x_values  # y 轴与 x 轴相同
z_values = np.full_like(x_values, 0.5)  # z 轴的值固定为 0.1

# 将 x, y, z 轴的数据结合
combined_data = np.column_stack((x_values, y_values, z_values))

# 统计行数
num_rows = combined_data.shape[0]
print("接收器数量：", num_rows)
print("接收器坐标：\n", combined_data)

# 保存到文件
with open(filepath + 'rcv.dat', 'w') as f:
    f.write(f'{num_rows}\n')  # 写入行数
    for data in combined_data:
        f.write(f"{data[0]:.1f} {data[1]:.1f} {data[2]:.1f}\n")
