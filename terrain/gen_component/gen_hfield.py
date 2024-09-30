import numpy as np


rows, cols = 100, 100

height_data = np.random.rand(rows * cols).astype(np.float32)
print(height_data)

with open("data/height_field.bin", "wb") as f:

    f.write(np.array([rows], dtype=np.int32).tobytes())
    f.write(np.array([cols], dtype=np.int32).tobytes())

    f.write(height_data.tobytes())
