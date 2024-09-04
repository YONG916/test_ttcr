import numpy as np
import matplotlib.pyplot as plt
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\2D_builder\\output\\"

data_name = ["model2d_tt_tertiary_nodes_1_src_radus_teriary_1.dat", "model2d_tt_tertiary_nodes_10_src_radus_teriary_10.dat"]
# data_name = ["model2d_tt_fsm_high_order_0.dat", "model2d_tt_fsm_high_order_1.dat"]
# data_name = ["model2d_tt_secondary_nodes_0.dat", "model2d_tt_secondary_nodes_1.dat", "model2d_tt_secondary_nodes_2.dat", "model2d_tt_secondary_nodes_10.dat"]
# 绘制折线图
plt.figure(figsize=(10, 6))
for name in data_name:
    data1 = np.loadtxt(filepath + name)
    plt.plot(data1, label=name, marker='o')

# 设置 x 轴为整数索引
plt.xticks(ticks=np.arange(0, len(data1), 1))
# 添加标题和标签
plt.title('Comparison of Time Data')
plt.xlabel('Index of Receiver')
plt.ylabel('Time Value')
plt.legend()
plt.grid(True)

# 显示图形
plt.show()
