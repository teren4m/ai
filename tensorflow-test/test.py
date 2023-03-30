from file_storage import file_storage as fs
import numpy as np

img = np.zeros((100, 100, 3))
img1 = np.zeros((101, 100, 3))
img2 = np.zeros((102, 100, 3))
fs.save_img('some',0, img)
fs.save_img('some',1, img1, metadata={'some':'some'})
# print(fs.save_img('some1',1, img, metadata={}))
# print(fs.save_img('some',1, img1))
# print(fs.save_img('some',2, img2))

info = fs.get_info_by_key_index('some', 1)
info.metadata = {'some':'new'}
fs.update_info(info)
info_new = fs.get_info_by_key_index('some', 1)
print(info_new)
