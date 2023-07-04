import matplotlib.pyplot as plt
import numpy as np

width=int(input('输入宽度'))
height=int(input('输入高度'))

# 生成一个随机的彩色图像
img = np.random.rand(height, width, 3)

# 绘制彩色图像
plt.imshow(img)

# 显示图像
plt.show()