import os, sys, inspect
import numpy as np

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir + "/../../")

METHODS = ["seq", "wy1", "wy2", "yty1", "yty2", "numpy", "Niliou's seq"]

RESULTS = "/results"

def timeMyMethods(n,m,p, method, num=3):
    from func import createBlockedToeplitz, testFactorization
    import timeit
    SETUP = """from func import createBlockedToeplitz; from ToeplitzFactorizor import ToeplitzFactorizor;
n = {0}; m = {1}; p = {2};
method = '{3}';
T = createBlockedToeplitz(n, m);
c = ToeplitzFactorizor(T, m);"""
    setup = SETUP.format(n,m,p,method)
    t = timeit.repeat('c.fact(method, p)', setup, number = num)
    return np.mean(t), np.std(t)

def timeNiliou(n,m,p, method, num=3):
    from func import createBlockedToeplitz, testFactorization
    import timeit
    SETUP = """from func import createBlockedToeplitz; from toeplitz_decomp import toeplitz_blockschur;
n = {0}; m = {1}; p = {2};
method = '{3}';
T = createBlockedToeplitz(n, m);"""
    setup = SETUP.format(n,m,p,method)
    t = timeit.repeat('toeplitz_blockschur(T, m, 0)', setup, number = num)
    return np.mean(t), np.std(t)

def timeNumpy(n,m,p, num=3):
    from func import createBlockedToeplitz, testFactorization
    import timeit
    SETUP = """from func import createBlockedToeplitz;
from scipy import linalg
n = {0}; m = {1}; p = {2};
T = createBlockedToeplitz(n, m);"""
    setup = SETUP.format(n, m, p, method)
    t = timeit.repeat('linalg.cholesky(T)', setup, number = num)
    return np.mean(t), np.std(t)


n = int(sys.argv[1])
m = int(sys.argv[2])
p = int(sys.argv[3])
num = int(sys.argv[4]) ## number of time to test
thread = int(sys.argv[5])
npr = int(sys.argv[6])

writeTo = currentdir
try:
    writeTo = os.environ["WRITE_TO"]
except:
    sys.stderr.write("Save location at: " + currentdir + "\n")

path = writeTo + RESULTS

data = np.array([[n,m,p,thread, npr, None, None]])
if not os.path.exists(path):
    os.makedirs(path)
    

for method in METHODS:
    if method in METHODS[:5]:
        t, t_err = timeMyMethods(n,m, p, method, num)
    if method == METHODS[5]:
        t, t_err = timeNumpy(n,m,p,num)
    if method == METHODS[6]:
        t, t_err = timeNiliou(n,m,p, num)
    data[0][-2] = t
    data[0][-1] = t_err
    with open(path + "/{0}.txt".format(method),'a') as f_handle:
        np.savetxt(f_handle,data)
