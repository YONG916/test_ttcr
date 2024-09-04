import numpy as np
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\3D_builder\\input\\"

# 定义数组的尺寸
nx, ny, nz = 50, 50, 50

# 初始化三维数组
slowness_array = np.zeros((nx, ny, nz))

# 设置慢度值
slowness_array[:, :, :10] = 6.666666666666666444e-04  # 0-20层
slowness_array[:, :, 10:30] = 4.000000000000000192e-04  # 20-40层
slowness_array[:, :, 30:] = 2.857142857142857357e-04  # 40-100层

# 保存到文件
output_file = 'model3d.slo'
with open(filepath + output_file, 'w') as f:
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                f.write(f'{slowness_array[i, j, k]:.16e}\n')
