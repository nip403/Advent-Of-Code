import numpy as np

def magnitudevec(vector: np.ndarray) -> float:
    return np.sqrt(np.sum(vector ** 2))

def unitvec(vector: np.ndarray) -> np.ndarray:
    return (vector / magnitudevec(vector)).astype(float)

def is_coincident(a: np.ndarray, b: np.ndarray) -> bool: # if vectors are a multiple of one another
    return abs(1 - ((np.dot(a, b) ** 2) / (np.dot(a, a) * np.dot(b, b)))) < 1e-6 # absolute tolerance, overload with relative in specific cases