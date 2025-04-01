import torch
from diffusers import SanaPipeline
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
    if os.path.exists('prompt.txt'):
        with open('prompt.txt', 'r',encoding="utf-8") as f:
            prompts = [line.strip() for line in f 
                      if line.strip() and not line.startswith('#')]
    else:
        raise FileNotFoundError("未找到prompt.txt文件")

num_iterations = args.num
total_runs = len(prompts) * num_iterations

# 初始化模型
pipe = SanaPipeline.from_pretrained(
    "Efficient-Large-Model/Sana_1600M_2Kpx_BF16_diffusers",
    variant="bf16",
    torch_dtype=torch.bfloat16,
    device_map="balanced",
)
pipe.vae.to(torch.bfloat16)
pipe.text_encoder.to(torch.bfloat16)
pipe.enable_vae_tiling()

# 生成循环
for prompt_idx, prompt in enumerate(prompts):
    for i in range(num_iterations):
        # 生成图像
        seed = random.randint(1, 100000000)
        image = pipe(
            prompt=prompt,
            height=2560,
            width=1440,
            guidance_scale=5,
            num_inference_steps=20,
            generator=torch.Generator().manual_seed(seed),
        )[0][0]
        
        # 保存图像
        filename = f"{prompt[:50]}_{seed}.png"
        image.save(filename)
        
        # 显示进度
        current_run = prompt_idx * num_iterations + i + 1
        print(f"[{current_run}/{total_runs}] 已生成: {filename}")

print("所有任务完成！")
