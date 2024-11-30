import os
import time
from PIL import Image

def compress_jpeg_files(directory):
    # 使用glob查找所有jpeg文件
    jpeg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                jpeg_files.append(os.path.join(root, file))

    # 遍历所有jpeg文件
    for file_path in jpeg_files:
        file_size = os.path.getsize(file_path)
        if file_size > 4 * 1024 * 1024:  # 检查文件大小是否大于4MB
            try:
                with Image.open(file_path) as img:
                    # 压缩并覆盖原文件
                    img.save(file_path, "JPEG", quality=90)
                    print(f"Compressed and overwrote: {file_path}")
            except Exception as e:
                print(f"Failed to compress {file_path}: {e}")

def main():
    while True:
        compress_jpeg_files('.')  # 扫描当前目录及其子目录
        time.sleep(10)  # 等待10秒

if __name__ == "__main__":
    main()
