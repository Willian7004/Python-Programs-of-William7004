import os
import pandas as pd

def process_csv_files():
    # 获取当前目录下所有CSV文件
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    for file in csv_files:
        try:
            # 读取CSV文件
            df = pd.read_csv(file)
            
            if df.empty:
                print(f"文件 {file} 是空的，跳过处理")
                continue
            
            # 找出所有以'count'开头的列（不区分大小写）
            count_columns = [col for col in df.columns if col.lower().startswith('count')]
            
            if not count_columns:
                print(f"文件 {file} 中没有以'count'开头的列，跳过处理")
                continue
            
            # 记录原始行数
            original_rows = len(df)
            
            # 对每个count列筛选出值大于等于100的行
            for col in count_columns:
                # 确保列是数值类型
                if pd.api.types.is_numeric_dtype(df[col]):
                    df = df[df[col] >= 100]
                else:
                    print(f"文件 {file} 中的列 {col} 不是数值类型，跳过该列")
            
            # 保存处理后的文件
            df.to_csv(file, index=False)
            print(f"处理文件 {file}: 原始行数 {original_rows}, 处理后行数 {len(df)}")
            
        except Exception as e:
            print(f"处理文件 {file} 时出错: {str(e)}")

if __name__ == "__main__":
    process_csv_files()
    print("处理完成")