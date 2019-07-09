
import sys
import time

import numpy as np
import scipy.sparse

from sklearn.datasets import load_svmlight_file


def convert_np_binary(path, X_file_stem, y_file_stem):
    """Load svmlight format file and dump as numpy binary
    Sparse matrix is saved with suffix .npz
    1-dim ndarray is saved with suffix .npy
    """

    X, y = load_svmlight_file(path, zero_based=True) 
    
    X_file_name = "{}.npz".format(X_file_stem)
    y_file_name = "{}.npy".format(y_file_stem)
    scipy.sparse.save_npz(X_file_name, X)
    np.save(y_file_name, y)


def load_np_binary(X_path, y_path):
    """Load binary file of sparse matrix and ndarray label
    Assuming their sample sizes are equal.
    """
    X = scipy.sparse.load_npz(X_path)
    y = np.load(y_path)
    assert X.shape[0] == y.shape[0]
    return X, y
