import numpy as np
from scipy import linalg


#H = np.array([[0, 0.5, 0.5, 0, 0, 0],
#              [0, 0, 0, 0, 0, 0],
#              [1/3.0, 1/3.0, 0, 0, 1/3.0, 0],
#              [0, 0, 0, 0, 0.5, 0.5],
#              [0, 0, 0, 0.5, 0, 0.5],
#              [0, 0, 0, 1, 0, 0]])
  

def pageRank(H, alpha=0.9):

    row_sums = H.sum(axis=1)
    for i, s in enumerate(row_sums):
        if s > 0:
            H[i] /= s
    length = H.shape[0]  

    H[np.all(H == 0, axis=1)] = np.ones(length) / length

    E = np.ones(H.shape) / length
    G = alpha * H + (1-alpha) * E
    assert np.allclose(np.sum(G, axis=1), 1)
    
    eigenvals, eigenvectors, _ = linalg.eig(G, left=True)
    result = None
    for i, val in enumerate(eigenvals):
        if np.isclose(val.real, 1) and np.isclose(val.imag, 0):
            result = eigenvectors[:, i]

    for i, val in enumerate(result):
        assert np.isclose(val.imag, 0)

    assert np.all(result > 0)
    return result.astype(np.dtype(np.float32))

