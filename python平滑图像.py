import numpy as np
import matplotlib.pyplot as plt

def color_difference(color1, color2):
    return abs(color1[0] - color2[0]) + abs(color1[1] - color2[1]) + abs(color1[2] - color2[2])

# 设置图像尺寸和颜色差异阈值
width = 48
height = 48
color_difference_threshold = 48

# 初始化全零数组作为基本的RGB图像
image_data = np.zeros((height, width, 3), dtype=np.uint8)

# 填充像素，同时确保颜色差异不超过阈值
for i in range(height):
    for j in range(width):
        # 如果是边界上的点，则只考虑现有邻近像素的颜色限制。
        neighbors = []
        if i > 0:
            neighbors.append(image_data[i-1, j])
        if j > 0:
            neighbors.append(image_data[i, j-1])

        while True:
            # 随机生成一个[0,255]之间的颜色
            new_color = np.random.randint(0, 256, size=3)

            # 检查新颜色与所有邻居的差值是否都小于color_difference_threshold
            all_differences_ok = True
            for neighbor in neighbors:
                if color_difference(new_color, neighbor) > color_difference_threshold:
                    all_differences_ok = False
                    break

            if all_differences_ok:
                image_data[i, j] = new_color
                print(new_color)
                break

# 使用Matplotlib显示图像
plt.imshow(image_data)
plt.show()