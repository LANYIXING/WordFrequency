import pandas as pd
a = ['a','b','c']
a.decode("utf8", "ignore")
del a[1]
a.append('d')
print(a)