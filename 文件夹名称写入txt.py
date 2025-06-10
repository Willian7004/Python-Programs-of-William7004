#写一个python程序，获取当前目录下所有文件夹的每次并写入txt文件，每个文件夹的名称占一行
import os

# 获取当前目录下的所有文件夹
folders = [f for f in os.listdir('.') if os.path.isdir(f)]

# 将文件夹名称写入txt文件
with open('folders_list.txt', 'w', encoding='utf-8') as f:
    for folder in folders:
        f.write(folder + '\n')

print(f"已完成，共写入 {len(folders)} 个文件夹名称到 folders_list.txt 文件")