import numpy as np

def reshape(a):
    if a.shape[0] % 2 != 0:
        raise RuntimeError('Expected a multiple of 2 but got an array of length {}'.format(a.shape[0]))
    n = int(a.shape[0]/2)
    return np.reshape(a, (n,2))

PEP = reshape(np.fromstring('''
  0.15 1.99
  0.3  2.10
  0.45 2.09
  0.6  1.84
  0.8  2.31
  5.5  2.76
 12    3.05
 21.5  2.42
 31.5  2.23
 61    2.52
 90    2.81
120.5  2.71
180.5  2.71
300.5  2.70
''', dtype=np.dtype('d'), sep=' '))

G6P = reshape(np.fromstring('''
  0.15 4.39
  0.3  4.76
  0.45 4.86
  0.6  4.65
  0.8  4.75
  5.5  5.52
 12    5.86
 21.5  4.39
 31.5  3.60
 61    3.83
 90    4.30
120.5  4.05
180.5  3.27
300.5  3.38
''', dtype=np.dtype('d'), sep=' '))

PYR = reshape(np.fromstring('''
  0.15 4.07
  0.3  3.71
  0.45 3.19
  0.6  3.57
  0.8  3.14
  5.5  2.38
 12    3.71
 21.5  3.19
 31.5  5.24
 61    4.47
 90    3.62
120.5  3.62
180.5  2.86
300.5  2.40
''', dtype=np.dtype('d'), sep=' '))

F6P = reshape(np.fromstring('''
  0.15 0.62
  0.3  0.66
  0.45 0.74
  0.6  0.62
  0.8  0.75
  5.5  0.92
 12    1.15
 21.5  0.57
 31.5  0.46
 61    0.57
 90    0.57
120.5  0.69
180.5  0.46
300.5  0.46
''', dtype=np.dtype('d'), sep=' '))

GLCex = reshape(np.fromstring('''
  5.5  1.256
 13.5  1.311
 31    1.283
 61    0.861
 91    0.597
151    0.096
181    0.043
212.5  0.051
241    0.048
270.5  0.048
301    0.06
''', dtype=np.dtype('d'), sep=' '))

G1P = reshape(np.fromstring('''
  2    1.35
 16    0.83
 19    0.83
 31    0.78
 57    0.84
 91.5  0.64
150.5  0.74
299    0.70
''', dtype=np.dtype('d'), sep=' '))

x6PG = reshape(np.fromstring('''
  3.5  1.01
  4    0.92
 12    1.15
 12.25 1.19
 21    1.06
 25.75 1.10
 30    1.05
 32.25 1.08
 58.5  0.97
 59    1.01
119.75 0.92
124    0.89
178    0.74
180    0.88
209    0.80
''', dtype=np.dtype('d'), sep=' '))

FDP = reshape(np.fromstring('''
  4.5  0.19
 11    0.56
 20    1.06
 30    2.83
 60    1.50
 90    2.26
119.5  2.40
180    1.25
239.5  0.07
300    0.02
''', dtype=np.dtype('d'), sep=' '))

GAP = reshape(np.fromstring('''
 0    0.22
 4.5   0.28
 11   0.32
 20   0.31
 30   0.24
 60   0.30
 90   0.18
119.5 0.22
180   0.21
239.5 0.22
300   0.20
''', dtype=np.dtype('d'), sep=' '))

# all data
data_quantities = [PEP, G6P, PYR, F6P, GLCex, G1P, x6PG, FDP, GAP]