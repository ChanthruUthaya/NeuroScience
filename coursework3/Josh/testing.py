import numpy as np

a = np.arange(0,10,1)
X =0
def func():
    global X
    for i in range(len(a)):
        a[i] += 1
        X += 1
        print(X)

print(a)
for i in range(0,10):
    func()
    F = 7
print(F)
print(a)
print(X)