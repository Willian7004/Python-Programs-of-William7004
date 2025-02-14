import os
import gc
import torch
from safetensors import torch as safetensors_torch

def convert_pt_to_safetensors():
    # 获取当前目录中的所有.pt文件
    current_dir = os.getcwd()
    pt_files = [f for f in os.listdir(current_dir) if f.endswith('.pt')]

    for pt_file in pt_files:
        file_path = os.path.join(current_dir, pt_file)
        try:
            # 使用cpu加载以减少GPU内存使用
            data = torch.load(file_path, map_location='cpu')
            
            # 提取张量数据
            if isinstance(data, torch.nn.Module):
                state_dict = data.state_dict()
            elif isinstance(data, dict):
                # 过滤非张量数据
                state_dict = {k: v for k, v in data.items() if isinstance(v, torch.Tensor)}
                if not state_dict:
                    print(f"Skipping {pt_file}: No tensors found.")
                    continue
            else:
                print(f"Skipping {pt_file}: Unsupported data type {type(data)}")
                continue

            # 生成输出路径
            output_path = os.path.splitext(file_path)[0] + '.safetensors'
            
            # 保存为safetensors格式
            safetensors_torch.save_file(state_dict, output_path)
            print(f"Successfully converted: {pt_file}")

            # 主动释放内存
            del data
            del state_dict
            
        except Exception as e:
            print(f"Failed to convert {pt_file}: {str(e)}")
        
        # 强制垃圾回收
        gc.collect()

if __name__ == "__main__":
    convert_pt_to_safetensors()