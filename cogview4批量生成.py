import torch
from diffusers import CogView4Pipeline
import random
import argparse
import os

# 参数解析
parser = argparse.ArgumentParser()
parser.add_argument('prompts', nargs='*', help='生成图像的提示词（可多个）')
parser.add_argument('--num', type=int, default=1, help='每个提示词的执行次数')
args = parser.parse_args()

# 处理提示词输入
if args.prompts:
    prompts = args.prompts
else:
    if os.path.exists('提示词.txt'):
        with open('提示词.txt', 'r',encoding="utf-8") as f:
            prompts = [line.strip() for line in f 
                      if line.strip() and not line.startswith('#')]
    else:
        raise FileNotFoundError("未找到提示词.txt文件")

num_iterations = args.num
total_runs = len(prompts) * num_iterations

# 初始化模型
pipe = CogView4Pipeline.from_pretrained("./CogView4-6B", torch_dtype=torch.bfloat16)

# Open it for reduce GPU memory usage
pipe.enable_sequential_cpu_offload()
pipe.vae.enable_slicing()
pipe.vae.enable_tiling()

# 生成循环
for prompt_idx, prompt in enumerate(prompts):
    for i in range(num_iterations):
        # 生成图像
        seed = random.randint(0, 99999)
        image = pipe(
            prompt=prompt,
            guidance_scale=3.5,
            num_images_per_prompt=1,
            num_inference_steps=30,
            width=1920,
            height=1088,
        ).images[0]
        
        # 保存图像
        filename = f"{prompt[:200]}_{seed}.png"
        image.save(filename)
        
        # 显示进度
        current_run = prompt_idx * num_iterations + i + 1
        print(f"[{current_run}/{total_runs}] 已生成: {filename}")

print("所有任务完成！")
