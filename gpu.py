# 创建 test_cuda.py 文件
# gpu.py 和 train.py 的顶部
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 允许重复加载
os.environ["OMP_NUM_THREADS"] = "1"  # 禁用多线程
os.environ["MKL_NUM_THREADS"] = "1"  # 禁用多线程

import torch

print("CUDA 是否可用:", torch.cuda.is_available())
print("可用 GPU 数量:", torch.cuda.device_count())
print("当前 GPU 名称:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "无")