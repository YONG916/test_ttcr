import pandas as pd
import numpy as np
from mayavi import mlab
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from model import *

#region S1.读取数据
filepath = "D:\\Nut_cloud\\C_program\\1_PointCloud\\package\\ttcr\\build4\\bin\\x64\\Debug\\3D_builder\\output\\"
# 文件名列表
# file_list = [
#     "model3d_src1_all_tt_spm_sencondary_nodes_0.dat",
#     "model3d_src1_all_tt_spm_sencondary_nodes_1.dat",
# ]

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

src = [0.5, 0.5, 0.5]
rcv = [45.5, 45.5, 0.5]

# 选择你要显示的文件名
selected_file = file_list[1]
file_path = filepath + selected_file

for selected_file in file_list:
    file_path = filepath + selected_file
    show_profile(selected_file, file_path)