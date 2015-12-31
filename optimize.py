
sys.setrecursionlimit(3000000)

output = {}
r7 = 1

def f_6027 (m,n):
    if (m,n) in output: return output[(m,n)]
    if m == 0:
        a = (n+1)%32768
    elif n == 0:
        a = f_6027(m-1,r7)
    else:
        a = f_6027(m, n-1)
        a = f_6027(m-1, a)
    output [(m,n)] = a
    return a

def f_6027_2 (m,n):
    s = []
    output = {}
    s.append(m)
    while s:
        m = s.pop()
        if m == 0:
            n = (n+1)%32768
        elif n == 0:
            n = r7
            s.append(m-1)
        else:
            n -= 1
            s.append(m-1)
            s.append(m)
    return n

print (f_6027(4,1), len(output))