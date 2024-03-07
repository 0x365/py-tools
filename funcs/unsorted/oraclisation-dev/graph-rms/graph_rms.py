import matplotlib.pyplot as plt
import numpy as np
import math

def get_rms(avg, m):
    return m-avg

def get_rms_comb(rms1, rms2):
    return math.sqrt(rms1*rms1 + rms2*rms2)


# for i in range(0, 100,10):
#     rms_comb_li = []
#     i_li = []
#     for ii in range(0, 100,10):
#         avg = (i + ii)/2
#         rms1 = get_rms(avg, i)
#         rms2 = get_rms(avg, ii)
#         #rms3 = get_rms(avg, iii)
#         rms_comb = get_rms_comb(rms1, rms2)
#         rms_comb_li.append(rms_comb)
#         i_li.append(avg)

# plt.plot(i_li, rms_comb_li, label=str(i))

y = []
x = []
for i in range(0,100):
    x.append(i)
    y.append(math.sqrt(2*i*i))
plt.plot(y,x)

    

plt.ylabel('RMS')
plt.xlabel('Distance Between Values (% of whole)')
#plt.legend()
plt.savefig(r"/home/robert/oraclisation-dev/src/graph-rms/graph.jpg")