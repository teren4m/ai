from numba import cuda
cuda.select_device(0)
cuda.close()