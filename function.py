a = 6095
b = 22160

mask = ((1<<15)-1)

_or = lambda x,y: (x|y) & mask
_and = lambda x,y: (x&y) & mask
_not = lambda x: (~x) & mask

print ("{:15b}".format(a))
print ("{:15b}".format(b))

print ("{:15b}".format(_and(_or(a,b),_not(_and(a,b)))))