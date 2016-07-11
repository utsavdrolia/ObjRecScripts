from collections import Counter

from pulp import *
sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/")
from PyCache.ZipfGenerator import ZipfGenerator

N = 500
print ("N:{}".format(N))

cloudcomput_const = 1  # 400 images in 400ms
network_latency = 70 # ms
network_bw = 5.0/8 # MBps
request_size = 50.0/1000 # MB per image
nw_lat = network_latency + (request_size / network_bw) * 1000
L = nw_lat + cloudcomput_const * N
print ("L:{}".format(L))

l = 2.0 # 2ms/object
print ("l:{}".format(l))

# Working set size
w = int(0.75*N)
# w = int(L/l)
# w = 100
print ("w:{}".format(w))

# generate zipf
z = ZipfGenerator(w, 0.5)
counter = Counter()
for i in range(100):
    counter[z.next()] += 1
countersum = sum(counter.values())
X_NUM = w
PROBS = []

for i in range(w):
    if i in counter.keys():
        PROBS.append(float(counter[i])/countersum)
    else:
        PROBS.append(0.0)
print sum(PROBS)
l = 2.0
L = 600.0

prob = LpProblem(name="Cache", sense=LpMinimize)
x_vars = LpVariable.dicts("x", [i for i in range(X_NUM)], 0, 1, cat='Integer')
#
# # lp1x1 + lp2x2 + lp3x3...
# var_sum = LpAffineExpression(e=[(x_vars[i],l*PROBS[i]) for i in range(X_NUM)])

exps = []
# sigma(x_i(l-L*p_i) + L*p_i)
for i in range(X_NUM):
    exps.append(LpAffineExpression(e=[(x_vars[i], l - L*PROBS[i])], constant=L*PROBS[i]))

costfunction = lpSum(exps)
print costfunction
prob.setObjective(costfunction)
prob.solve()
print("Status:", LpStatus[prob.status])
cachesize = 0
for i in range(X_NUM):
    print value(x_vars[i])
    cachesize += value(x_vars[i])

print ("Cache Size:{}".format(cachesize))