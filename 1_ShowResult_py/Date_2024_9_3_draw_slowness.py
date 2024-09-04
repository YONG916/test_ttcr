import numpy as np
from mayavi import mlab
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\3D_builder\\input\\"
filename= "model3d.slo"
full_path = filepath + filename
nx, ny, nz = 50, 50, 50

# 初始化一个空的 3D 数组
data_3d = np.zeros((nx, ny, nz))

# 读取文件
with open(full_path, 'r') as file:
    lines = file.readlines()

# 逐列读取数据并填充到 3D 数组中
index = 0
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            data_3d[i, j, k] = float(lines[index].strip())
            index += 1



#region 可视化
mlab.figure(size=(800, 600))
source = mlab.pipeline.scalar_field(1/data_3d)  # scalar_field获得数据的标量数据场
source.spacing = [1, 1, 1]
for axis in ['x', 'y', 'z']:  # x,y,z代表了3个剖面
    plane = mlab.pipeline.image_plane_widget(source,  # ，画剖面
                                             plane_orientation='{}_axes'.format(axis),  ##设置切平面的方向
                                          slice_index=0, colormap='gray', transparent=True, opacity=0.1)
# 设置坐标轴标签
mlab.xlabel('X')
mlab.ylabel('Y')
mlab.zlabel('Z')

plane.module_manager.scalar_lut_manager.reverse_lut = True  # 反转颜色映射
# 添加颜色条
mlab.show()

#endregion