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