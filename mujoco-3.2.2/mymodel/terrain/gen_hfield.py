import numpy as np

# 定义高场的大小
rows, cols = 100, 100
# 生成一些随机高度数据
height_data = np.random.rand(rows * cols).astype(np.float32)
print(height_data)

# 创建二进制文件
with open("data/height_field.bin", "wb") as f:
    # 写入行数和列数
    f.write(np.array([rows], dtype=np.int32).tobytes())
    f.write(np.array([cols], dtype=np.int32).tobytes())
    # 写入高度数据
    f.write(height_data.tobytes())
