'''
写一个python程序，把当前目录下所有flac文件转换为128kbps的mp3文件并覆盖原文件
'''
import os
import subprocess
from pathlib import Path

def convert_flac_to_mp3(input_file, output_file, bitrate='128k'):
    """使用ffmpeg将FLAC文件转换为MP3"""
    try:
        subprocess.run([
            'ffmpeg',
            '-i', input_file,
            '-codec:a', 'libmp3lame',
            '-b:a', bitrate,
            '-y',  # 覆盖输出文件而不询问
            output_file
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {input_file} - {e}")
        return False
    except FileNotFoundError:
        print("错误: 未找到ffmpeg。请确保已安装ffmpeg并添加到系统PATH中。")
        return False

def main():
    # 获取当前目录下所有.flac文件
    flac_files = list(Path('.').glob('*.flac'))
    
    if not flac_files:
        print("当前目录下未找到任何FLAC文件。")
        return
    
    print(f"找到 {len(flac_files)} 个FLAC文件，开始转换...")
    
    for flac_file in flac_files:
        mp3_file = flac_file.with_suffix('.mp3')
        print(f"正在转换: {flac_file} -> {mp3_file}")
        
        if convert_flac_to_mp3(str(flac_file), str(mp3_file)):
            # 转换成功，删除原FLAC文件
            try:
                flac_file.unlink()
                print(f"转换完成，已删除原文件: {flac_file}")
            except OSError as e:
                print(f"警告: 无法删除原文件 {flac_file} - {e}")
    
    print("所有文件处理完成。")

if __name__ == "__main__":
    main()