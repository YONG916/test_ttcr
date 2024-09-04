import ttcrpy.rgrid as rg
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 创建网格
x = np.arange(51.0)
y = np.arange(51.0)
z = np.arange(51.0)

# 三维速度模型
# 速度沿z方向线性变化
a = 1.0
V20 = 3.0
b = (V20-a)/20.0

V = np.empty((x.size, y.size, z.size))
for n in range(z.size):
    V[:, :, n] = a + b*z[n]

# 画图，显示一下模型
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')

min_val = V.min()
max_val = V.max()
n_x, n_y, n_z = V.shape
colormap = plt.cm.plasma

cut = V[0,:,:]
Y, Z = np.mgrid[0:n_y, 0:n_z]
X = np.zeros((n_y, n_z))
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=colormap((cut-min_val)/(max_val-min_val)), shade=False)
cut = V[:,-1,:]
X, Z = np.mgrid[0:n_x, 0:n_z]
Y = y[-1] + np.zeros((n_x, n_z))
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=colormap((cut-min_val)/(max_val-min_val)), shade=False)
cut = V[:,:,-1]
X, Y = np.mgrid[0:n_x, 0:n_y]
Z = z[-1] + np.zeros((n_x, n_y))
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=colormap((cut-min_val)/(max_val-min_val)), shade=False)
ax.invert_zaxis()
ax.set_title("Velocity model")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
fig.tight_layout()
plt.show()


# src and rcv should be 2D arrays
# 发射点和接收点的坐标

src = np.array([[0.5, 0.5, 0.5]])
x1, y1, z1 = np.arange(50.0), np.arange(50.0), np.arange(50.0)
X1, Y1, Z1 = np.meshgrid(x1, y1, z1, indexing='ij')
rcv =  np.array([[45.5, 45.5, 0.5]])

# slowness will de assigned to grid nodes, we must pass cell_slowness=False
# 慢度模型
grid = rg.Grid3d(x, y, z, cell_slowness=False, n_threads = 10, method='SPM')

# we need to input slowness
slowness = 1./V

import time
start = time.time()
tt, rays = grid.raytrace(src, rcv, slowness, return_rays=True)
print("Time taken: ", time.time()-start)

plt.figure(2)
plt.plot(tt, 'r-o')
plt.xlabel('Rcv number')
plt.ylabel('Traveltime')
# plt.show()

fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')
min_val = V.min()
max_val = V.max()
n_x, n_y, n_z = V.shape
colormap = plt.cm.plasma

cut = V[:,:,-1]
X, Y = np.mgrid[0:n_x, 0:n_y]
Z = z[-1] + np.zeros((n_x, n_y))
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=colormap((cut-min_val)/(max_val-min_val)), shade=False)

rays_part = rays[-50:]
for r in rays_part:
    ax.plot(r[:,0], r[:,1], r[:,2],'r-')

ax.invert_zaxis()
ax.set_title("Rays")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
ax.set_zlim(0, 50)
fig.tight_layout()

plt.show()
