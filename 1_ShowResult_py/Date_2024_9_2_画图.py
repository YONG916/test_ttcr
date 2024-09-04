import pandas as pd
import matplotlib.pyplot as plt

filepath = ("D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin"
            "\\x64\Debug\\2D_builder\\TestScripts\\TestResult\\")
filename = "runtime_TestTertiaryNodes.csv"
df = pd.read_csv(filepath + filename)

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(df[df.columns[0]], df['TotalTimeSeconds'], label='Total Run time', marker='o')
plt.plot(df[df.columns[0]], df['GridTimeSeconds'], label='Time to build grid with secondary nodes', marker='o')
plt.plot(df[df.columns[0]], df['RaytraceTimeSeconds'], label='Time to perform raytracing', marker='o')
plt.xlabel(df.columns[0])
plt.ylabel('Running Time (Seconds)')
plt.grid()
plt.legend()
plt.show()

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(df[df.columns[0]], df['SingleRayPathTime'], label='Average Run Time to Run Single Ray Path', marker='o')
plt.xlabel(df.columns[0])
plt.ylabel('Running Time (Seconds)')
plt.grid()
plt.legend()
plt.show()


