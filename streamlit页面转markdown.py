import os
import ast

class StreamlitTransformer(ast.NodeVisitor):
    def __init__(self):
        self.md_content = []
    
    def get_string_value(self, node):
        """从AST节点提取字符串值"""
        if node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.Str):  # 兼容Python3.7及以下
            return node.s
        return None
    
    def process_title(self, node):
        if node.args:
            title = self.get_string_value(node.args[0])
            if title:
                self.md_content.append(f"# {title}\n\n")
    
    def process_subheader(self, node):
        if node.args:
            subheader = self.get_string_value(node.args[0])
            if subheader:
                self.md_content.append(f"### {subheader}\n\n")
    
    def process_write(self, node):
        texts = []
        for arg in node.args:
            text = self.get_string_value(arg)
            if text:
                texts.append(text)
        if texts:
            self.md_content.append(f"{' '.join(texts)}\n\n")
    
    def process_image(self, node):
        # 获取图片路径
        path = self.get_string_value(node.args[0]) if node.args else None
        if not path:
            return
        
        # 获取caption
        caption = None
        for kw in node.keywords:
            if kw.arg == "caption":
                caption = self.get_string_value(kw.value)
                break
        
        # 生成Markdown图片语法
        self.md_content.append(f"![{caption or ''}]({path})\n\n")
    
    def visit_Call(self, node):
        # 检查是否为st的调用
        if isinstance(node.func, ast.Attribute):
            obj = node.func.value
            if isinstance(obj, ast.Name) and obj.id == "st":
                method = node.func.attr
                if method == "title":
                    self.process_title(node)
                elif method == "subheader":
                    self.process_subheader(node)
                elif method == "write":
                    self.process_write(node)
                elif method == "image":
                    self.process_image(node)
        self.generic_visit(node)

def convert_file(input_path, output_path):
    """转换单个文件"""
    with open(input_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        print(f"警告：文件 {input_path} 解析失败，已跳过")
        return
    
    transformer = StreamlitTransformer()
    transformer.visit(tree)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(transformer.md_content))

def main():
    # 配置输入输出目录
    current_dir = os.getcwd()
    pages_dir = os.path.join(current_dir, "pages")
    output_dir = os.path.join(current_dir, "markdown_output")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历并转换所有py文件
    for filename in os.listdir(pages_dir):
        if filename.endswith(".py"):
            input_path = os.path.join(pages_dir, filename)
            output_filename = filename.rsplit(".", 1)[0] + ".md"
            output_path = os.path.join(output_dir, output_filename)
            convert_file(input_path, output_path)
    
    print(f"转换完成！结果已保存至 {output_dir}")

if __name__ == "__main__":
    main()