'''
（基于comfyui官方api示例）
根据以下要求修改程序：
1. seed使用随机自然数
2. 在程序中按文件名顺序读取当前目录下所有 .md 文件，对每一行依次匹配“.”、“:”和“**”，匹配到则去掉匹配到的字符和前面的字符，把剩余内容填入prompt_text。在程序开头设置每个prompt的执行次数。
'''
import json
import random
import glob
from urllib import request

# 设置每个prompt的执行次数
execution_count = 2  # 可修改此值调整执行次数

prompt_text = """
{
  "3": {
    "inputs": {
      "seed": 686454193860211,
      "steps": 30,
      "cfg": 4,
      "sampler_name": "euler",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "13",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "12",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "K采样器"
    }
  },
  "6": {
    "inputs": {
      "text": "A teenage girl walking on street",
      "clip": [
        "10",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "7": {
    "inputs": {
      "text": "",
      "clip": [
        "10",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP文本编码"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "15",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE解码"
    }
  },
  "10": {
    "inputs": {
      "clip_name": "oldt5_xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "cosmos",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "加载CLIP"
    }
  },
  "12": {
    "inputs": {
      "width": 896,
      "height": 1600,
      "batch_size": 1
    },
    "class_type": "EmptySD3LatentImage",
    "_meta": {
      "title": "空Latent图像（SD3）"
    }
  },
  "13": {
    "inputs": {
      "unet_name": "cosmos_predict2_2B_t2i.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet加载器"
    }
  },
  "15": {
    "inputs": {
      "vae_name": "wan_2.1_vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载VAE"
    }
  },
  "28": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  }
}
"""

def queue_prompt(prompt):
    p = {"prompt": prompt}

    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)


prompt = json.loads(prompt_text)
# 读取所有.md文件并按文件名排序
md_files = sorted(glob.glob("*.md"))

# 处理每个文件
for file in md_files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 依次匹配标记
            content = None
            for marker in ['.', ':', '**']:
                if marker in line:
                    content = line.split(marker, 1)[1].strip()
                    break
            
            if content:
                # 多次执行带随机seed的prompt
                for _ in range(execution_count):
                    current_prompt = json.loads(prompt_text)
                    current_prompt["6"]["inputs"]["text"] = content
                    current_prompt["3"]["inputs"]["seed"] = random.randint(1, 10**9)
                    queue_prompt(current_prompt)
