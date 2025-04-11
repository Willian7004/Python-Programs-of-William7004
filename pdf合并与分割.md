### user:

写两个python程序，分别实现以下功能：

1.输入文件名，把当前目录下相应文件名的pdf文件分割为多个250页的部分，在原文件名后加序号并保存，序号形式为（1）、（2）

2.输入文件名（不含序号部分），把当前目录下相应文件名且文件名末尾有序号的多个pdf文件按序号顺序合并为一个pdf文件

### assistant:

# Python 程序 1: 分割 PDF 文件

```python
import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_pages():
    # 获取用户输入的文件名
    filename = input("请输入要分割的PDF文件名（包含扩展名）: ").strip()
    
    # 检查文件是否存在
    if not os.path.exists(filename):
        print(f"错误: 文件 '{filename}' 不存在!")
        return
    
    # 检查是否是PDF文件
    if not filename.lower().endswith('.pdf'):
        print("错误: 文件必须是PDF格式!")
        return
    
    try:
        # 读取PDF文件
        pdf_reader = PdfReader(filename)
        total_pages = len(pdf_reader.pages)
        
        # 计算需要分割成多少部分
        parts = (total_pages // 250) + (1 if total_pages % 250 else 0)
        
        if parts <= 1:
            print(f"文件只有 {total_pages} 页，不需要分割。")
            return
        
        print(f"文件共有 {total_pages} 页，将被分割为 {parts} 个部分。")
        
        # 分割文件
        base_name = filename[:-4]  # 去掉 .pdf 扩展名
        for i in range(parts):
            start_page = i * 250
            end_page = min((i + 1) * 250, total_pages)
            
            pdf_writer = PdfWriter()
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            output_filename = f"{base_name}（{i+1}）.pdf"
            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            
            print(f"已创建: {output_filename} (页 {start_page + 1}-{end_page})")
        
        print("分割完成!")
    
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

if __name__ == "__main__":
    split_pdf_by_pages()
```

# Python 程序 2: 合并 PDF 文件

```python
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
```

## 使用说明

1. **分割PDF程序**:
   - 输入要分割的PDF文件名（包含.pdf扩展名）
   - 程序会将文件按每250页分割，生成类似"原文件名(1).pdf", "原文件名(2).pdf"的文件

2. **合并PDF程序**:
   - 输入要合并的PDF文件的基础名（不包含序号部分）
   - 程序会查找当前目录下所有匹配"基础名(n).pdf"格式的文件，并按n的顺序合并

## 依赖安装

在运行这两个程序前，需要安装PyPDF2库:

```bash
pip install PyPDF2
```

注意：这两个程序都假设在当前目录下操作文件，且文件名中的序号格式为中文括号"（）"。