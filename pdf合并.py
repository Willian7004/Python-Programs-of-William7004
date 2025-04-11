import os
import re
from PyPDF2 import PdfMerger

def merge_pdf_with_numbered_parts():
    # 获取用户输入的文件名基础部分
    base_name = input("请输入要合并的PDF文件基础名（不含序号）: ").strip()
    
    # 准备正则表达式匹配带序号的文件
    pattern = re.compile(rf"^{re.escape(base_name)}（(\d+)）\.pdf$", re.IGNORECASE)
    
    # 查找匹配的文件
    matched_files = []
    for filename in os.listdir('.'):
        match = pattern.match(filename)
        if match:
            part_num = int(match.group(1))
            matched_files.append((part_num, filename))
    
    if not matched_files:
        print(f"没有找到以 '{base_name}（n）.pdf' 格式命名的文件。")
        return
    
    # 按序号排序文件
    matched_files.sort()
    
    print("找到以下文件将按顺序合并:")
    for part_num, filename in matched_files:
        print(f"{filename}")
    
    # 合并PDF文件
    merger = PdfMerger()
    output_filename = f"{base_name}.pdf"
    
    try:
        for _, filename in matched_files:
            merger.append(filename)
        
        with open(output_filename, 'wb') as output_pdf:
            merger.write(output_pdf)
        
        print(f"合并完成! 结果已保存为: {output_filename}")
    
    except Exception as e:
        print(f"合并过程中发生错误: {e}")
    finally:
        merger.close()

if __name__ == "__main__":
    merge_pdf_with_numbered_parts()