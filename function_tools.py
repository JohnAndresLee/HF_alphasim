import numpy as np 
from numba import jit

@jit(nopython=True)
def compute_mean(arr, axis, step):
    num_slices = arr.shape[axis] // step
    if axis == 0:
        shape = (num_slices, arr.shape[1] , arr.shape[2])
    elif axis == 1:
        shape = (arr.shape[0], num_slices, arr.shape[2])
    elif axis == 2:
        shape = (arr.shape[0], arr.shape[1], num_slices)
    else:
        raise ValueError ("Invalid axis.")

    means = np.empty(shape, dtype=np.float64)

    for i in range(0, arr.shape[0], step if axis == 0 else 1):
        for j in range(0, arr.shape[1], step if axis == 1 else 1): 
            for k in range(shape[2], step if axis == 2 else 1):
                if axis == 0:
                    slice_ = arr[i:i + step, j, k]
                    means[i//step, j, k] = np.mean(slice_)
                elif axis == 1:
                    slice_ = arr[i, j:j + step, k]
                    means[i, j // step, k] = np.mean(slice_)
                elif axis == 2:
                    slice_ = arr[i, j, k:k + step]
                    means[1, j, k // step] = np.mean(slice_)
    return means

@jit(nopython=True)
def compute_std(arr, axis, step):
    num_slices = arr.shape[axis] // step
    if axis == 0:
        shape = (num_slices, arr.shape[1], arr.shape[2])
    elif axis == 1:
        shape = (arr.shape[0], num_slices, arr.shape[2])
    elif axis == 2:
        shape = (arr.shape[0], arr.shape[1], num_slices) 
    else:
        raise ValueError ("Invalid axis.")
    
    stds = np.empty(shape, dtype=np.float64)

    for i in range(0, arr.shape[0], step if axis == 0 else 1):
        for j in range(0, arr.shape[1], step if axis == 1 else 1): 
            for k in range(shape[2], step if axis == 2 else 1):
                if axis == 0:
                    slice_ = arr[i:i + step, j, k]
                    stds[i // step, j, k] = np.std(slice_)
                elif axis == 1:
                    slice_ = arr[i, j:j + step, k]
                    stds[i, j // step, k] = np.std(slice_)
                elif axis == 2:
                    slice_ = arr[i, j, k:k + step]
                    stds[i, j, k // step] = np.std(slice_)
    return stds

@jit(nopython=True)
def compute_skew(arr, axis, step):
    num_slices = arr.shape[axis] // step
    if axis == 0:
        shape = (num_slices, arr.shape[1], arr.shape[2])
    elif axis == 1:
        shape = (arr.shape[0], num_slices, arr.shape[2])
    elif axis == 2:
        shape = (arr.shape[0], arr.shape[1], num_slices) 
    else:
        raise ValueError ("Invalid axis.")
    
    skews = np. empty(shape, dtype=np.float64)
    
    for i in range(0, arr.shape[0], step if axis == 0 else 1):
        for j in range(0, arr.shape[1], step if axis == 1 else 1):
            for k in range(shape[2], step if axis == 2 else 1):
                if axis == 0:
                    slice_ = arr[i:i + step, j, k]
                    m3 = np.mean((slice_ - np.mean(slice_)) ** 3)
                    skews [i // step, j, k] = m3 / (np.std(slice_)**3) if np.std(slice_) != 0 else 0
                elif axis == 1:
                    slice_ = arr[1, j:j + step, k]
                    m3 = np.mean ((slice_ - np.mean(slice_)) ** 3)
                    skews [i, j // step, k] = m3 / (np.std(slice_)**3) if np.std(slice_) != 0 else 0
                elif axis == 2:
                    slice_ = arr[i, j, k:k + step]
                    m3 = np.mean ((slice_ - np.mean(slice_)) ** 3)
                    skews [i, j, k // step] = m3 / (np.std(slice_)**3) if np.std(slice_) != 0 else 0
    return skews
            
@jit(nopython=True)
def compute_kurt(arr, axis, step):
    num_slices = arr.shape[axis] // step
    if axis == 0:
        shape = (num_slices, arr.shape[1], arr.shape[2])
    elif axis == 1:
        shape = (arr.shape[0], num_slices, arr.shape[2])
    elif axis == 2:
        shape = (arr.shape[0], arr.shape[1], num_slices)
    else:
        raise ValueError ("Invalid axis.")
    
    kurts = np. empty(shape, dtype=np.float64)

    for i in range(0, arr.shape[0], step if axis == 0 else 1):
        for j in range(0, arr.shape[1], step if axis == 1 else 1): 
            for k in range(shape[2], step if axis == 2 else 1):
                if axis == 0:
                    slice_ = arr[i:i + step, j, k]
                    m4 = np.mean ((slice_ - np.mean(slice_)) ** 4)
                    kurts[i // step, j, k] = m4 / (np.std(slice_) ** 4) -3 if np.std(slice_) != 0 else 0
                elif axis == 1:
                    slice_ = arr[i, j:j + step, k]
                    m4 = np.mean ((slice_ - np.mean(slice_)) ** 4)
                    kurts[i, j // step, k] = m4 / (np.std(slice_) ** 4) -3 if np.std(slice_) != 0 else 0
                elif axis == 2:
                    slice_ = arr[i, j, k:k + step]
                    m4 = np.mean ((slice_ - np.mean (slice_)) ** 4)
                    kurts[i, j, k // step] = m4 / (np.std(slice_) ** 4) -3 if np.std(slice_) != 0 else 0
    return kurts