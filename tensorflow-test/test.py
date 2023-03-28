import file_storage as fs
import numpy as np

img = np.zeros((100, 100, 3))
print(fs.save_img('some', img))
