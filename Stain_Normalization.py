from sklearn.utils import shuffle
import pandas as pd
import os
import spams
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import io

os.environ["CUDA_VISIBLE_DEVICES"] = '0'


class TissueMaskException(Exception):
    pass


######################################################################################################

def is_uint8_image(I):
    if not is_image(I):
        return False
    if I.dtype != np.uint8:
        return False
    return True


######################################################################################################

def is_image(I):
    if not isinstance(I, np.ndarray):
        return False
    if not I.ndim == 3:
        return False
    return True


######################################################################################################
# 通过亮度阈值得到主要组织的掩码
def get_tissue_mask(I, luminosity_threshold=0.8):
    I_LAB = cv2.cvtColor(I, cv2.COLOR_RGB2LAB)
    L = I_LAB[:, :, 0] / 255.0  # Convert to range [0,1].
    mask = L < luminosity_threshold

    # Check it's not empty
    if mask.sum() == 0:
        raise TissueMaskException("Empty tissue mask computed")

    return mask


######################################################################################################
# 转换RGB到OD
def convert_RGB_to_OD(I):
    mask = (I == 0)
    I[mask] = 1

    # return np.maximum(-1 * np.log(I / 255), 1e-6)
    return np.maximum(-1 * np.log(I / 255), np.zeros(I.shape) + 0.1)


######################################################################################################
# 转换OD到RGB
def convert_OD_to_RGB(OD):
    assert OD.min() >= 0, "Negative optical density."

    OD = np.maximum(OD, 1e-6)

    return (255 * np.exp(-1 * OD)).astype(np.uint8)


######################################################################################################

def normalize_matrix_rows(A):
    return A / np.linalg.norm(A, axis=1)[:, None]


######################################################################################################

# 得到浓度
def get_concentrations(I, stain_matrix, regularizer=0.01):
    OD = convert_RGB_to_OD(I).reshape((-1, 3))
    # 稀疏优化
    return spams.lasso(X=OD.T, D=stain_matrix.T, mode=2, lambda1=regularizer, pos=True).toarray().T


######################################################################################################

def get_stain_matrix(I, luminosity_threshold=0.8, angular_percentile=99):
    # assert is_uint8_image(I), "Image should be RGB uint8."
    # 转换为OD并忽略背景
    tissue_mask = get_tissue_mask(I, luminosity_threshold=luminosity_threshold).reshape((-1,))
    OD = convert_RGB_to_OD(I).reshape((-1, 3))

    OD = OD[tissue_mask]

    # Eigenvectors of cov in OD space (orthogonal as cov symmetric)
    # OD空间中cov的特征向量（正交为cov对称）
    _, V = np.linalg.eigh(np.cov(OD, rowvar=False))

    # The two principle eigenvectors
    # 两个主要的特征向量
    V = V[:, [2, 1]]

    # Make sure vectors are pointing the right way
    # 确保向量指向正确的方向
    if V[0, 0] < 0: V[:, 0] *= -1
    if V[0, 1] < 0: V[:, 1] *= -1

    # Project on this basis.
    That = np.dot(OD, V)

    # Angular coordinates with repect to the prinicple, orthogonal eigenvectors
    # 相对于主要的正交特征向量的角度坐标
    phi = np.arctan2(That[:, 1], That[:, 0])

    # Min and max angles
    minPhi = np.percentile(phi, 100 - angular_percentile)
    maxPhi = np.percentile(phi, angular_percentile)

    # the two principle colors
    v1 = np.dot(V, np.array([np.cos(minPhi), np.sin(minPhi)]))
    v2 = np.dot(V, np.array([np.cos(maxPhi), np.sin(maxPhi)]))

    # Order of H and E.
    # H first row.
    if v1[0] > v2[0]:
        HE = np.array([v1, v2])
    else:
        HE = np.array([v2, v1])

    return normalize_matrix_rows(HE)


######################################################################################################

def mapping(target, source):
    stain_matrix_target = get_stain_matrix(target)
    target_concentrations = get_concentrations(target, stain_matrix_target)
    maxC_target = np.percentile(target_concentrations, 99, axis=0).reshape((1, 2))
    stain_matrix_target_RGB = convert_OD_to_RGB(stain_matrix_target)

    stain_matrix_source = get_stain_matrix(source)
    source_concentrations = get_concentrations(source, stain_matrix_source)
    maxC_source = np.percentile(source_concentrations, 99, axis=0).reshape((1, 2))
    source_concentrations *= (maxC_target / maxC_source)
    tmp = 255 * np.exp(-1 * np.dot(source_concentrations, stain_matrix_target))
    return tmp.reshape(source.shape).astype(np.uint8)

source_dir='/home/ty/docker/ty/chenkairun/an_img/test/'
target = cv2.imread('/home/ty/docker/ty/chenkairun/an_img/goal.png')
# Convert from cv2 standard of BGR to our convention of RGB.
target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

for fname in os.listdir(source_dir):
    fpath=os.path.join(source_dir,fname)
    source = cv2.imread(fpath)
    # Convert from cv2 standard of BGR to our convention of RGB.
    source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
    # Perform stain normalization
    transformed = mapping(target,source)
    io.imsave('/home/ty/docker/ty/chenkairun/an_img/test_result/'+fname,transformed)
cv2.waitKey()
