import numpy as np
a = np.arange(0,60,5)
print(a)
a = a.reshape(3,4)
print(a)
#使用nditer迭代器,并使用for进行遍历
for x in np.nditer(a):
   print(x)
   
b = a.T
print(b)

for x in np.nditer(b):
   print(x)
   
c = a.T.copy(order = 'F')
for x in np.nditer(c):
   print (x, end=", " )
   
d = np.arange(9).reshape(3,3)
for row in d:
    print (row)
#使用flat属性：
for ele in d.flat:
    print (ele,end="，")