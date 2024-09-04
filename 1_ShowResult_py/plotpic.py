import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 读取CSV文件
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\Debug\\runtime_results.csv"
df = pd.read_csv(filepath)

# 绘制折线图
plt.figure(figsize=(10, 6))

# 绘制 RuntimeSeconds 折线
plt.plot(df['SecondaryNodes'], df['RuntimeSeconds'], label='RuntimeSeconds', marker='o')

# 绘制 AllPointRunTime 折线
# plt.plot(df['SecondaryNodes'], df['AllPointRunTime'], label='AllPointRunTime', marker='o')
# 设置y轴的刻度
plt.yticks(np.arange(0, 10, 0.5))

# 添加标题和标签
plt.title('1 source and 20 receivers')
plt.xlabel('Secondary Nodes')
plt.ylabel('Running Time (Seconds)')
plt.legend()

# 显示网格
plt.grid(True)

# 显示图形
plt.show()
