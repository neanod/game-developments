from pickle import *

f = open('save.pickle', 'wb')
dump(0, f)
f.close()