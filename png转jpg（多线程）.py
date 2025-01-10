import os
import concurrent.futures
from PIL import Image
import shutil

def convert_png_to_jpeg(png_path, jpeg_path):
    """将PNG文件转换为JPEG文件"""
    try:
        with Image.open(png_path) as img:
            img.convert('RGB').save(jpeg_path, 'JPEG')
        print(f"Converted: {png_path} -> {jpeg_path}")
    except Exception as e:
        print(f"Failed to convert {png_path}: {e}")

def process_directory(root_dir, output_dir):
    """遍历目录并处理PNG文件"""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png'):
                png_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, root_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                jpeg_path = os.path.join(output_subdir, os.path.splitext(file)[0] + '.jpg')
                yield png_path, jpeg_path

def main():
    root_dir = 'v2'
    output_dir = 'v2_converted'

    if not os.path.exists(root_dir):
        print(f"Directory '{root_dir}' does not exist.")
        return

    # 获取CPU核心数
    num_threads = os.cpu_count()

    # 使用线程池并行处理文件转换
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for png_path, jpeg_path in process_directory(root_dir, output_dir):
            futures.append(executor.submit(convert_png_to_jpeg, png_path, jpeg_path))

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()

