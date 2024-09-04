import matplotlib.pyplot as plt
import numpy as np
from model import *

root_path = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\3D_builder\\"
file_input_path = root_path + "input\\"
file_ouput_path = root_path + "output\\"

# 文件名列表
file_list = [
    "model3d_src1_all_tt_fsm_high_order_0.dat",
    "model3d_src1_all_tt_fsm_high_order_1.dat",
    "model3d_src1_all_tt_fsm_iteration20.dat",
    "model3d_src1_all_tt_fsm_iteration100.dat",
    "model3d_src1_all_tt_spm_sencondary_nodes_0.dat",
    "model3d_src1_all_tt_spm_sencondary_nodes_1.dat",
    "model3d_src1_all_tt_tertiary_nodes_1_src_radius_tertiary_1.dat",
    "model3d_src1_all_tt_tertiary_nodes_10_src_radius_tertiary_10.dat"
]

# file_list = [
#     "model3d_src1_all_tt_spm_sencondary_nodes_0.dat",
#     "model3d_src1_all_tt_spm_sencondary_nodes_1.dat",
# ]




# region读取初始文件
# 读取rcv文件
with open(file_input_path + "rcv.dat", 'r') as f:
    num_rows_rcv = int(f.readline().strip())
    rcv_data = [list(map(float, f.readline().strip().split())) for _ in range(num_rows_rcv)]

# 读取src文件
with open(file_input_path + "src1.dat", 'r') as f:
    num_rows_src = int(f.readline().strip())
    src_data = [list(map(float, f.readline().strip().split())) for _ in range(num_rows_src)]


# 读取.grd文件
# 读取文件

with open(file_input_path + "model3d.grd", 'r') as f:
    # 读取并解析每一行
    number_of_cells = list(map(int, f.readline().split('#')[0].strip().split()))
    size_of_cells = list(map(int, f.readline().split('#')[0].strip().split()))
    origin_of_grid = list(map(int, f.readline().split('#')[0].strip().split()))
# 计算 nx, ny, nz
nx = number_of_cells[0] - origin_of_grid[0] + 1
ny = number_of_cells[1] - origin_of_grid[1] + 1
nz = number_of_cells[2] - origin_of_grid[2] + 1

dx, dy, dz = size_of_cells[0], size_of_cells[1], size_of_cells[2]
src = src_data[0].copy()

# 初始化一个空的 3D 数组
data_3d = np.zeros((nx - 1, ny - 1, nz - 1))

# 读取文件
filename= "model3d.slo"
full_path = file_input_path + filename
with open(full_path, 'r') as file:
    lines = file.readlines()
# 逐列读取数据并填充到 3D 数组中
index = 0
for i in range(nx - 1):
    for j in range(ny - 1):
        for k in range(nz - 1):
            data_3d[i, j, k] = float(lines[index].strip())
            index += 1
# endregion
alpha = 1
for selected_file in file_list:

    # region 计算射线轨迹
    for rcv in rcv_data:
        file_path = file_ouput_path + selected_file
        print("selected_file: ", selected_file)
        data = pd.read_csv(file_path, sep='\s+', header=None, names=['z', 'y', 'x', 'tt'])
        T = np.array(data["tt"]).reshape((nx, ny, nz))
        ray_x, ray_y, ray_z = ray_tracing_3D(T, src, rcv, dx, dy, dz)
        ray_x.append(src[0])
        ray_y.append(src[1])
        ray_z.append(src[2])

    # endregion

    plot_slowness_with_raypath(alpha, data_3d, ray_x, ray_y, ray_z, selected_file, src, rcv,
                                   save_path='Img\\img_slowness_raypath\\')

    #endregion

