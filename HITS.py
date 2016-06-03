import numpy as np
from scipy import linalg

#L = np.array([[0, 1, 1, 0, 0, 0],
#              [0, 0, 0, 0, 0, 0],
#              [1, 1, 0, 0, 1, 0],
#              [0, 0, 0, 0, 1, 1],
#              [0, 0, 0, 1, 0, 1],
#              [0, 0, 0, 1, 0, 0]])

def HITS(L):
    eigenvals, eigenvectors = linalg.eig(np.dot(L, L.T), right=True)

    #ovo valjda radi ok (mozda treba apsolutne vrijednosti od eigenvals)
    h = eigenvectors[:, np.argmax(eigenvals)]

    for i, val in enumerate(h):
        assert np.isclose(val.imag, 0)

    eigenvals, eigenvectors = linalg.eig(np.dot(L.T, L), right=True)
    
    a = eigenvectors[:, np.argmax(eigenvals)]

    for i, val in enumerate(a):
        assert np.isclose(val.imag, 0)

    a = a.astype(np.dtype(np.float32)) / np.linalg.norm(a, ord=1)
    h = h.astype(np.dtype(np.float32)) / np.linalg.norm(h, ord=1)

    #assert np.all(a >= 0)
    #assert np.all(h >= 0)

    return a, h

