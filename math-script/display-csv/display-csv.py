import numpy as np
import matplotlib.pyplot as plt
import csv
import struct

'''
CSV fomat:
1.558804150,2,0x0003
1.558815500,1,0xFFF7
1.558826850,2,0x0007
'''

# display range
x_start = 2000
x_end   = 3000

x_list = []
y_list = []
with open('i2s.csv') as f:
    rows = csv.reader(f)
    rows.__next__() # skip first line

    for row in rows:
        time  = row[0]
        ch    = row[1]
        value = int(row[2], 10)
        value = (value & ((1 << 15) - 1)) - (value & (1 << 15))
        if ch == '1':
            x_list.append(float(time))
            y_list.append(value)
            # print(float(time), value)

# x = np.array(x_list)0
x = np.arange(0, len(y_list))
y = np.array(y_list)

x = x[x_start:x_end]
y = y[x_start:x_end]
plt.plot(x, y)
plt.show()

# scale_val = 256
# sample_rate = 16000
# sin_freq = 10
# half_scale = scale_val/2

# x = np.arange(0, 16000)
# y = half_scale * np.sin(x*sin_freq*(2*np.pi)/sample_rate) + half_scale
# plt.plot(x, y)
# plt.show()
