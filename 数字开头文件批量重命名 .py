import os
import re

def increment_filenames(n):
    # 获取当前目录下所有.py文件
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    
    for filename in files:
        # 使用正则表达式匹配文件名开头的数字
        match = re.match(r'^(\d+)', filename)
        if not match:
            continue  # 跳过不以数字开头的文件
        
        current_num = int(match.group(1))
        if current_num >= n:
            new_num = current_num + 1
            # 替换文件名开头的数字部分
            new_filename = re.sub(r'^\d+', str(new_num), filename, count=1)
            # 重命名文件
            os.rename(filename, new_filename)
            print(f'Renamed "{filename}" to "{new_filename}"')

if __name__ == "__main__":
    n = int(input("Enter a number: "))
    increment_filenames(n)
