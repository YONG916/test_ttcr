import pandas as pd
import numpy as np
from mayavi import mlab
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def show_profile(selected_file, file_path):
    print("selected_file: ", selected_file)
    # 使用 pandas 读取文件
    # 交换了x与z的位置
    data = pd.read_csv(file_path, sep='\s+', header=None, names=['z', 'y', 'x', 'tt'])

    # 显示前几行数据
    # print(data.head())
    #endregion


    # # region S2. 三维可视化
    # # 交换了x与z的位置
    # x = data['x'].astype(int).values
    # y = data['y'].astype(int).values
    # z = data['z'].astype(int).values
    # tt = data['tt'].values
    #
    # # 找到网格的范围
    # nx, ny, nz = x.max() + 1, y.max() + 1, z.max() + 1
    #
    # # 创建3D数组，用于存储标量场
    # scalar_field = np.zeros((nx, ny, nz))
    #
    # # 将tt值填充到3D数组中
    # scalar_field[x, y, z] = tt
    #
    # # 使用 Mayavi 创建源对象，直接使用原始数据
    # source = mlab.pipeline.scalar_field(scalar_field)
    #
    # # 绘制沿 x, y, z 轴的切片
    # for axis in ['x', 'y', 'z']:  # x, y, z代表了3个剖面
    #     plane = mlab.pipeline.image_plane_widget(source,
    #                                              plane_orientation='{}_axes'.format(axis),
    #                                              slice_index=scalar_field.shape[{'x': 0, 'y': 1, 'z': 2}[axis]] // 2,
    #                                              colormap='coolwarm',  # 设置配色方案
    #                                              transparent=True,
    #                                              opacity=0.7)
    #
    # # 设置坐标轴标签
    # mlab.xlabel('X')
    # mlab.ylabel('Y')
    # mlab.zlabel('Z')
    #
    # # 显示图形
    # mlab.show()
    # #endregion

    # region S3. 二维可视化
    x = data['x'].astype(int).values
    y = data['y'].astype(int).values
    z = data['z'].astype(int).values
    tt = data['tt'].values
    # 假设数据已经读取到 `data` 中，且 `nx`, `ny`, `nz` 已定义
    nx, ny, nz = x.max() + 1, y.max() + 1, z.max() + 1
    # 筛选出的剖面条件
    profile_x, profile_y, profile_z = 0, 0, 0
    conditions = [
        (data['x'] == profile_x),
        (data['y'] == profile_y),
        (data['z'] == profile_z),
        (data['x'] == data['y'])
    ]

    # 剖面的标题
    titles = ['x = ' + str(profile_x), 'y = ' + str(profile_y), 'z = ' + str(profile_z), 'x = y']

    # 设置图表
    fig, axs = plt.subplots(1, 4, figsize=(32, 6))
    fig.suptitle(f'File: {selected_file}', fontsize=16)
    for i, condition in enumerate(conditions):
        # 筛选出满足条件的剖面数据
        slice_data = data[condition]

        # 根据不同的剖面，提取对应的 x, z, tt 数据
        if i == 0:  # x = 0.5
            x = slice_data['y'].values.reshape(ny, nz)
            z = slice_data['z'].values.reshape(ny, nz)
        elif i == 1:  # y = 0.5
            x = slice_data['x'].values.reshape(nx, nz)
            z = slice_data['z'].values.reshape(nx, nz)
        elif i == 2:  # z = 0.5
            x = slice_data['x'].values.reshape(nx, ny)
            z = slice_data['y'].values.reshape(nx, ny)
        elif i == 3:  # x = y
            x = slice_data['x'].values.reshape(nx, nz)
            z = slice_data['z'].values.reshape(nx, nz)

        tt = slice_data['tt'].values.reshape(x.shape)

        # 绘制等值线图
        cs = axs[i].contourf(x, z, tt, levels=14, cmap="RdBu_r")
        axs[i].set_title(f'travel time to first arrival at {titles[i]}')
        axs[i].set_xlabel('x' if i != 0 else 'y')
        axs[i].set_ylabel('z')

        # 设置相同的长宽比
        axs[i].set_aspect('equal')

        # 翻转z轴（y轴在2D图中表示z轴）
        axs[i].invert_yaxis()

        # 绘制等值线
        contours = axs[i].contour(x, z, tt, levels=14, colors='black', linewidths=0.5)

        # 在等值线中显示数值
        axs[i].clabel(contours, inline=True, fontsize=8, fmt="%.2f")

    # 添加颜色条
    fig.colorbar(cs, ax=axs, orientation='vertical', fraction=0.05)

    # img_tt_profile
    save_path = 'Img\\img_tt_profile\\' + selected_file + '.png'
    plt.savefig(save_path, dpi=300)  # 设置分辨率为300 DPI
    plt.show()


def ray_tracing_3D(T, source, receiver, dx, dy, dz):
    # 初始化
    current_pos = np.array(receiver)
    ray_x = [current_pos[0]]
    ray_y = [current_pos[1]]
    ray_z = [current_pos[2]]

    # 计算梯度
    dTdx, dTdy, dTdz = np.gradient(T, dx, dy, dz)

    while np.linalg.norm(current_pos - source) > max(dx, dy, dz):
        # 获取当前点的索引
        ix = int(round(current_pos[0] / dx))
        iy = int(round(current_pos[1] / dy))
        iz = int(round(current_pos[2] / dz))

        # 边界检查
        if ix < 0 or ix >= T.shape[1] or iy < 0 or iy >= T.shape[0] or iz < 0 or iz >= T.shape[2]:
            break

        # 获取梯度
        grad_T = np.array([dTdx[iy, ix, iz], dTdy[iy, ix, iz], dTdz[iy, ix, iz]])

        # 计算步进方向（沿梯度的反方向）
        step_direction = -grad_T / np.linalg.norm(grad_T)

        # 更新位置
        current_pos += step_direction * min(dx, dy, dz)

        # 记录射线位置
        ray_x.append(current_pos[0])
        ray_y.append(current_pos[1])
        ray_z.append(current_pos[2])

    return ray_x, ray_y, ray_z


def plot_slowness_with_raypath(alpha, data_3d, ray_x, ray_y, ray_z, selected_file, src, rcv,
                               save_path='Img\\img_slowness_raypath\\'):
    # 创建 3D 图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 在顶部添加标题，即文件名
    plt.title(selected_file, pad=20)

    # 定义 colormap 和 normed_slowness 函数
    min_slow, max_slow = 1 / data_3d.max(), 1 / data_3d.min()
    colormap = plt.cm.Greys

    def normed_slowness(slowness):
        return (slowness - min_slow) / (max_slow - min_slow)

    # 绘制 Z=50 处的平面
    nx, ny, nz = data_3d.shape
    X, Y = np.meshgrid(range(nx), range(ny))
    Z = np.full_like(X, nz - 1)
    slowness_plane_Z = 1 / data_3d[:, :, nz - 1]
    slowness_plane_Z = normed_slowness(slowness_plane_Z)
    ax.plot_surface(X, Y, Z, facecolors=colormap(slowness_plane_Z), alpha=alpha, rstride=1, cstride=1, shade=False)

    # 绘制 Y=50 处的平面
    X, Z = np.meshgrid(range(nx), range(nz))
    Y = np.full_like(X, ny - 1)
    slowness_plane_Y = 1 / data_3d[:, ny - 1, :]
    slowness_plane_Y = normed_slowness(slowness_plane_Y)
    ax.plot_surface(X, Y, Z, facecolors=colormap(slowness_plane_Y.T), alpha=alpha, rstride=1, cstride=1, shade=False)

    # 绘制 X=0 处的平面
    Y, Z = np.meshgrid(range(ny), range(nz))
    X = np.full_like(Y, 0)
    slowness_plane_X = 1 / data_3d[0, :, :]
    slowness_plane_X = normed_slowness(slowness_plane_X)
    ax.plot_surface(X, Y, Z, facecolors=colormap(slowness_plane_X.T), alpha=alpha, rstride=1, cstride=1, shade=False)

    # 绘制射线轨迹
    ax.plot(ray_x, ray_y, ray_z, color='r', zorder=10, linewidth=2)

    # 绘制起点和终点（如果需要的话可以取消注释）
    # ax.scatter([src[0]], [src[1]], [src[2]], zorder=10, color='g', s=50, label='Source')
    # ax.scatter([rcv[0]], [rcv[1]], [rcv[2]], zorder=10, color='g', s=50, label='Receiver')

    # 设置轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 设置坐标轴范围与刻度（可根据需要调整）
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)

    # 翻转 Z 轴
    ax.set_zlim(50, 0)  # 翻转 Z 轴，使其从上往下

    # 保存图形
    plt.savefig(f'{save_path}{selected_file}.png')

    # 显示图形
    plt.show()


# if mask_mayavi:
#     #region S2.绘制3D射线
#     from mayavi import mlab
#
#     # 设置figure大小
#     mlab.figure(size=(800, 600))
#
#     # 绘制数据的剖面视图
#     source = mlab.pipeline.scalar_field(1/data_3d)
#     source.spacing = [1, 1, 1]
#     # 假设 source 是你已经创建好的标量场
#
#
#     # x 和 y 轴的切片索引为 0，z 轴的切片索引为 nz
#     slice_indices = {'x': nx, 'y': 0, 'z': nz}
#
#     for axis in ['x', 'y', 'z']:
#         plane = mlab.pipeline.image_plane_widget(
#             source,
#             plane_orientation=f'{axis}_axes',
#             slice_index=slice_indices[axis],
#             colormap='gray',
#             transparent=True,
#             opacity=0.1
#         )
#
#     plane.module_manager.scalar_lut_manager.reverse_lut = True
#     # 设置轴标签
#     mlab.xlabel('X')
#     mlab.ylabel('Y')
#     mlab.zlabel('Z')
#
#     # 绘制三维射线轨迹
#     mlab.plot3d(ray_x, ray_y, ray_z, tube_radius=None, line_width=2.0, color=(1, 0, 0))
#
#     # 绘制起点和终点
#     mlab.points3d([src[0], rcv[0]], [src[1], rcv[1]], [src[2], rcv[2]],
#                   color=(0, 1, 0), scale_factor=1.0)
#
#     # 设定视角
#     azimuth, elevation, distance, focalpoint = mlab.view()
#     print(azimuth, elevation, distance, focalpoint)
#     mlab.view(azimuth=90, elevation=0, distance=distance, focalpoint=[25, 25, 25])
#
#     # mlab.pitch(degrees=15)
#     # mlab.pitch(degrees=45)
#     # save_path = 'img_tt_profile\\' + selected_file + '.png'
#     # # 保存当前视图为PNG图像
#     # mlab.savefig(save_path)
#
#     # 显示图形
#     mlab.show()
#     # print(mlab.view())
#     #endregion