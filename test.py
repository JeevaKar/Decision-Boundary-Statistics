import pandas as pd
import itertools
from stats import longestdistance, merge, avgDist, border, regressionDegree
import matplotlib.pyplot as plt
from math import comb
from datetime import datetime
import os

# df = pd.read_csv(r"old.csv")
df = pd.read_csv(r"new.csv")
# df = df.iloc[::1000, :]
df = df.sample(frac=1)

start_time = datetime.now()

x = list(df.iloc[:, 0])  # First column (x)
y = list(df.iloc[:, 1])  # Second column (y)
z = list(df.iloc[:, 2])  # Third column (z)

df_0 = df[df['0'] == 0]  # Rows where 4th column is 0
df_1 = df[df['0'] == 1]  # Rows where 4th column is 1

# defining all 3 axis
x0 = list(df_0.iloc[:, 0])  # First column (x)
y0 = list(df_0.iloc[:, 1])  # Second column (y)
z0 = list(df_0.iloc[:, 2])  # Third column (z)

x1 = list(df_1.iloc[:, 0])
y1 = list(df_1.iloc[:, 1])
z1 = list(df_1.iloc[:, 2])

all_lists = [x, y, z]
distanceMetric = 1-avgDist(x0, y0, z0, x1, y1, z1)/longestdistance(merge(all_lists))
combinations = itertools.combinations(all_lists, 2)

borderxy, borderyx = border(points1=merge([x0,y0]), points2=merge([x1,y1]), xmax=256, ymax=256, xmin=0, ymin=0, step=1)
borderyz, borderzy = border(points1=merge([y0,z0]), points2=merge([y1,z1]), xmax=256, ymax=256, xmin=0, ymin=0, step=1)
borderxz, borderzx = border(points1=merge([x0,z0]), points2=merge([x1,z1]), xmax=256, ymax=256, xmin=0, ymin=0, step=1)

tempx, tempy = zip(*borderxy)
degxy, BICxy = regressionDegree(tempx, tempy)

tempx, tempy = zip(*borderyz)
degyz, BICyz = regressionDegree(tempx, tempy)

tempx, tempy = zip(*borderxz)
degxz, BICxz = regressionDegree(tempx, tempy)

tempx, tempy = zip(*borderyx)
degyx, BICyx = regressionDegree(tempx, tempy)

tempx, tempy = zip(*borderzy)
degzy, BICzy = regressionDegree(tempx, tempy)

tempx, tempy = zip(*borderzx)
degzx, BICzx = regressionDegree(tempx, tempy)

if degyx < degxy:
    degxy = degyx
    BICxy = BICyx
if degzy < degyz:
    degyz = degzy
    BICyz = BICzy
if degzx < degxz:
    degxz = degzx
    BICxz = BICzx

n=10
BICScore = ((degxy/n)+(degyz/n)+(degxz/n))/3

end_time = datetime.now()
elapsed_time = end_time - start_time

os.system('cls' if os.name == 'nt' else 'clear')
print(f"Elapsed time: {elapsed_time}")
print("Distance Metric: "+str(distanceMetric))
print("Degrees: "+str(degxy)+" "+str(degyz)+" "+str(degxz))
print("BICs: "+str(BICxy)+" "+str(BICyz)+" "+str(BICxz))
print("Bic Score: "+str(BICScore))

x, y = zip(*borderxz)

plt.plot(x0,z0,'o')
plt.plot(x1,z1,'o')
plt.plot(x,y)
plt.show()