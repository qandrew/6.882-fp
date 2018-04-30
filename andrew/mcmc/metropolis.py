import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# boltmann
def q(x, y):
  g1 = mlab.bivariate_normal(x, y, 1.0, 1.0, -1, -1, -0.8)
  g2 = mlab.bivariate_normal(x, y, 1.5, 0.8, 1, 2, 0.6)
  return 0.6*g1+28.4*g2/(0.6+28.4)

# def q(x,y):
#   # if (x**2 - 5)
#   # print x, y
#   print "\n"
#   print x,y
#   print type(x), type(y)
#   if 0 < x and x < 5 and 0 < y and y < 5:
#     return 0.3  
#   else:
#     z =  1/(abs(x - 2.5) + abs(y - 2.5))
#     # print z
#     return z


'''Metropolis Hastings'''
N = 100
s = 10
r = np.zeros(2) #x_0
p = q(r[0], r[1])
print "p = ", p
samples = []
for i in xrange(N):
  rn = r + np.random.normal(size=2)
  pn = q(rn[0], rn[1])
  if pn >= p: #accept
    p = pn
    r = rn
  else:
    u = np.random.rand()
    if u < pn/p:
      p = pn
      r = rn
    # else reject
  if i % s == 0:
    samples.append(r)

samples = np.array(samples)
plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5, s=1)

'''Plot target'''
dx = 0.01
x = np.arange(np.min(samples), np.max(samples), dx)
y = np.arange(np.min(samples), np.max(samples), dx)
print x.shape, y.shape
X, Y = np.meshgrid(x, y)
print "\n"
print X
print X.shape
print "\n"
print Y
print Y.shape

Z = q(X, Y)
print "\n"
print Z
print Z.shape
print type(Z)
CS = plt.contour(X, Y, Z, 10)
plt.clabel(CS, inline=1, fontsize=10)
plt.show()