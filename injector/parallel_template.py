
import numpy as np
import string
import tqdm
import hashlib
def chunks(l, n):
    """ Yield n successive chunks from l.
    """
    newn = int(len(l) / n)
    for i in xrange(0, n-1):
        yield l[i*newn:i*newn+newn]
    yield l[n*newn-newn:]
def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.
    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.
    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.
    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])
    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

from multiprocessing import Pool
import time
from tqdm import *
from itertools import product
import string
import math
salt ='9614ba56553bd6a5707831ebed9395de81096571cbd1282b97a5755c21464072f4e890030ebd5111aef9e7cda18d4e75c503b28e0860d35e9bc3a45adc89e7dc'
correct='a6ab787fdace563008c45f14aa9d5da5e3c0ef41acfe76ec09212484ba641ee9fc228db69104d207ff32e4cdfd294be1300921143531977661bce7daef3b6433'
correct2='67f2fab154885054e661b4dc0c83cb4a0166a7c803668a9612eb1b52dce1d48cb2ad6d430830986946995342465cd7835365fa82e86aea5137d94e5bbc54b430'
correct3='91dfe7681c46f2042fa1b8c68901dd9afc12ccad7f6493e16c485db03d5594fb9df68718dbbbd0f90b1b9e91d751c8f065e5eaf1f9edf71d3683f5ba79d19f10'
def worker(totest):
    for i in tqdm(totest):
       hashed = hashlib.sha512(hashlib.sha512(i.tostring()).hexdigest()+salt).hexdigest()
       if hashed == correct:
           return i.tostring()
    return 'not found'

if __name__ == '__main__':

    allarr = []
    for i in range(4):
        allarr.append(list(string.ascii_lowercase+string.digits))
    result=cartesian(allarr)
    print('done cartesian')
    #chunks(result,40)
    print('done cart')
    p = Pool(processes=40)
    found = p.map(worker,chunks(result,40))
    p.close()
    p.join()
    print found
    for i in found:
        if i !='not found':
            print i
    #worker(result[:10])
