import numpy as np
A = np.array([[3,-1], [-1,3]])
print("A.shape=", A.shape) # 通过.shape可查看A的形状特征
print("A=", A)
B = np.dot(A, A)
print("B.shape=", B.shape,)
print("B=", B)
C = np.dot(B, A)
print("C.shape=", C.shape,)
print("C=", C)
D = np.dot(C, A)
print("D.shape=", D.shape,)
print("D=", D)
