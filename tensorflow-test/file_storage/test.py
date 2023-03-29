import file_storage as fs
import numpy as np

img = np.zeros((100, 100, 3))
img1 = np.zeros((101, 100, 3))
img2 = np.zeros((102, 100, 3))
print(fs.save_img('some',0, img))
print(fs.save_img('some',1, img1))
# print(fs.save_img('some1',1, img, metadata={}))
# print(fs.save_img('some',1, img1))
# print(fs.save_img('some',2, img2))

print(len(fs.get_img_by_key('some')))
