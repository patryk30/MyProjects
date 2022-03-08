# -*- coding: utf-8 -*-
"""
Przetwarzanie i analiza danych w programie Python - Projekt 2/3
Plik generujacy pliki .data oraz .labels ze zbiorami benchmarkowymi
"""

import numpy as np
import matplotlib.pyplot as plt

################ pierwszy zbior ########################
t1 = np.linspace(-5,5,500) + np.random.normal(0, 0.5, 500)
X1 = 16*(np.sin(t1)**3)
Y1 = -13*np.cos(t1) + 5*np.cos(2*t1) + 2*np.cos(3*t1) + np.cos(4*t1)

t2 = np.linspace(0,2*np.pi,300) + np.random.normal(0, 0.5, 300)
X2 = 4*np.sin(t2)-9
Y2 = 4*np.cos(t2)-5

t3 = np.linspace(0,2*np.pi,300) + np.random.normal(0, 0.5, 300)
X3 = 4*np.sin(t3)+9
Y3 = 4*np.cos(t3)-5

t4 = np.linspace(0,2*np.pi,300) + np.random.normal(0, 0.5, 300)
X4 = 4*np.sin(t4)
Y4 = 4*np.cos(t4)+1

X=np.concatenate([X1,X2,X3,X4])
Y=np.concatenate([Y1,Y2,Y3,Y4])

labels1 = np.concatenate([np.repeat(1,500),np.repeat(2,300),
                         np.repeat(3,300),np.repeat(4,300)])

data1 = np.zeros(shape=(1400,2))
data1[:,0] = X
data1[:,1] = Y

plt.scatter(data1[:,0], data1[:,1])

path1 = r"C:\Users\patry\OneDrive\Pulpit\Zdalne pw\Python - PadPy\Projekt_23_dane_benchmarkowe\\"


data1_file = path1+'zbior1.data.gz'
labels1_file = path1+'zbior1.labels0.gz'

np.savetxt(data1_file, data1, fmt="%1.4f")
np.savetxt(labels1_file, labels1, fmt="%1.4f")


################# drugi zbior #########################

A1 = 6 * np.random.random_sample((450,)) - 3
B1 = np.abs(A1)+np.random.normal(0, 0.1, 450) + 2

A2 = 6 * np.random.random_sample((300,)) - 6
B2 = -np.abs(A2+3)+np.random.normal(0, 0.25, 300) + 3

A=np.concatenate([A1,A2])
B=np.concatenate([B1,B2])

labels2 = np.concatenate([np.repeat(1,450),np.repeat(2,300)])

data2 = np.zeros(shape=(750,2))
data2[:,0] = A
data2[:,1] = B

data2_file = path1+'zbior2.data.gz'
labels2_file = path1+'zbior2.labels0.gz'

np.savetxt(data2_file, data2, fmt="%1.4f")
np.savetxt(labels2_file, labels2, fmt="%1.4f")



################### trzeci zbior #####################

fi = 2 * np.pi * np.random.random_sample((750,))
psi = np.pi * np.random.random_sample((750,)) - 0.5 *np.pi

XX1 = np.cos(fi)*np.cos(psi)
YY1 = np.sin(fi)*np.cos(psi)
ZZ1 = np.sin(psi)

alfa = 2 * np.pi * np.random.random_sample((500,))
XX2 = 1.5*np.cos(alfa) + np.random.normal(0, 0.1, 500)
YY2 = 1.5*np.sin(alfa) + np.random.normal(0, 0.1, 500)
ZZ2 = np.repeat(0.4,500)

alfa2 = 2 * np.pi * np.random.random_sample((500,))
ZZ4 = 2.5*np.cos(alfa2) + np.random.normal(0, 0.2, 500)
YY4 = 2.5*np.sin(alfa2) + np.random.normal(0, 0.2, 500)
XX4 = np.repeat(0.4,500)

XX=np.concatenate([XX1,XX2,XX4])
YY=np.concatenate([YY1,YY2,YY4])
ZZ=np.concatenate([ZZ1,ZZ2,ZZ4])

labels3 = np.concatenate([np.repeat(1,750),np.repeat(2,500),
                         np.repeat(3,500)])

data3 = np.zeros(shape=(1750,3))
data3[:,0] = XX
data3[:,1] = YY
data3[:,2] = ZZ

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

# Generate the values
x_vals = data3[:, 0]
y_vals = data3[:, 1]
z_vals = data3[:, 2]

# Plot the values
ax.scatter(x_vals, y_vals, z_vals, c = labels3 , marker='o')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')


data3_file = path1+'zbior3.data.gz'
labels3_file = path1+'zbior3.labels0.gz'

np.savetxt(data3_file, data3, fmt="%1.4f")
np.savetxt(labels3_file, labels3, fmt="%1.4f")





