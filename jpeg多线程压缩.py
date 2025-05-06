'''
写一个python程序，使用多线程，把当前目录下input文件夹以及子文件夹中的jpeg转换为高度1440、压缩比例85%的jpg文件，保存到output文件夹并保留目录结构。
'''
import os
import threading
from queue import Queue
from PIL import Image

def process_image(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            # 计算等比例缩放后的宽度
            width = int((1440 / img.height) * img.width)
            # 调整图片大小
            img = img.resize((width, 1440), Image.LANCZOS)
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # 保存为JPG格式，质量85%
            img.save(output_path, 'JPEG', quality=85)
            print(f"处理成功: {input_path} -> {output_path}")
    except Exception as e:
        print(f"处理失败 {input_path}: {str(e)}")

def worker(q):
    while True:
        input_path, output_path = q.get()
        try:
            process_image(input_path, output_path)
        finally:
            q.task_done()

def main():
    input_dir = "input"
    output_dir = "output"
    
    # 确保输入目录存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 '{input_dir}' 不存在")
        return
    
    # 创建线程池
    num_threads = 4  # 可以根据CPU核心数调整
    q = Queue()
    
    # 启动工作线程
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q,), daemon=True)
        t.start()
    
    # 遍历input目录及其子目录
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.jpeg', '.jpg')):
                input_path = os.path.join(root, file)
                # 构建输出路径，保留目录结构
                rel_path = os.path.relpath(root, input_dir)
                output_root = os.path.join(output_dir, rel_path)
                # 确保输出文件扩展名为.jpg
                output_file = os.path.splitext(file)[0] + '.jpg'
                output_path = os.path.join(output_root, output_file)
                
                # 将任务加入队列
                q.put((input_path, output_path))
    
    # 等待所有任务完成
    q.join()
    print("所有图片处理完成")

if __name__ == "__main__":
    main()