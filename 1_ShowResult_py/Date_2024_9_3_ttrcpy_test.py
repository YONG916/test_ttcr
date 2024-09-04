import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import ttcrpy.rgrid as rg
import time

# 创建网格
x = np.arange(201.0)
y = np.arange(201.0)
z = np.arange(101.0)

# 创建慢度模型
slowness = np.empty((x.size, y.size, z.size))
slowness[:, :, :20] = 6.666666666666666444e-04  # 0-20层
slowness[:, :, 20:40] = 4.000000000000000192e-04  # 20-40层
slowness[:, :, 40:] = 2.857142857142857357e-04  # 40-100层

# 计算速度
V = 1 / slowness

# 配置颜色映射
min_val = slowness.min()
max_val = slowness.max()




# 发射点和接收点的坐标
src = np.array([[0.5, 0.5, 0.5]])
x_values = np.linspace(70, 190, 20)
y_values = x_values.copy()
z_values = np.full_like(x_values, 1)  # z轴值固定为0.1
rcv = np.column_stack((x_values, y_values, z_values)) + 0.5

# 创建慢度模型的网格
grid = rg.Grid3d(x, y, z, cell_slowness=False, n_threads=10)

# 射线追踪
start_time = time.time()
tt, rays = grid.raytrace(src, rcv, slowness, return_rays=True)
print("Time taken: ", time.time() - start_time)



# 创建3D图形\
#region
fig = plt.figure()

def colormap(value):
    normed = (value - min_val) / (max_val - min_val)
    return cm.gray(normed)  # 灰度映射，归一化后翻转

ax = fig.add_subplot(111, projection='3d')
# 绘制每个切面
n_x, n_y, n_z = slowness.shape
# 第一个切面
cut1 = slowness[0,:,:]
Y, Z = np.mgrid[0:n_y, 0:n_z]
X = np.zeros((n_y, n_z)) - 2
ax.plot_surface(X, Y, Z, alpha = 0.5, rstride=1, cstride=1, facecolors=colormap(cut1), shade=False)

# 第二个切面
cut2 = slowness[:,-1,:]
X, Z = np.mgrid[0:n_x, 0:n_z]
Y = np.full((n_x, n_z), y[-1])
ax.plot_surface(X, Y, Z, alpha = 0.5, rstride=1, cstride=1, facecolors=colormap(cut2), shade=False)

# 第三个切面
cut3 = slowness[:,:,-1]
X, Y = np.mgrid[0:n_x, 0:n_y]
Z = np.full((n_x, n_y), z[-1])
ax.plot_surface(X, Y, Z, alpha = 0.5, rstride=1, cstride=1, facecolors=colormap(cut3), shade=False)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


for r in rays:
    ax.scatter(r[:,0], r[:,1], r[:,2],c='r',s=1)
ax.scatter(rcv[:, 0], rcv[:,1], rcv[:,2], c='b', s=20)
ax.scatter(src[0,0], src[0,1], src[0,2], c='g', s=20)
# 配置视图
ax.set_xlim(-10, 200)
ax.set_ylim(0, 200)
ax.set_zlim(0, 100)  # 翻转Z轴
ax.invert_zaxis()

plt.show()
#endregion
