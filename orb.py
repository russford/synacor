def gen_possibles (s, pos_x, pos_):
    poss = []
    if pos_x > 0: poss.append((-1,0))
    if pos_x < 3: poss.append((1,0))
    if pos_y > 0: poss.append((0,-1))
    if pos_y < 3: poss.append((0,1))

    return [(s+" "+str(a[pos_x+px][pos_y+py]), pos_x+px, pos_y+py) for px,py in poss]

def evaluate (s):
    l = s.split(" ")
    if len(l) % 2 == 0: return 0
    n = int (l[0])
    for i in range(len(l)//2):
        if l[i*2+1] == "+":
            n += int(l[i*2+2])
        elif l[i*2+1] == "-":
            n -= int(l[i*2+2])
        elif l[i*2+1] == "*":
            n *= int(l[i*2+2])
        else:
            return 0
    return n

class FoundException(Exception):
    pass

def check_prune (p):
    n = evaluate(p[0])
    if n == 0: return True
    if n > 70: return False
    if n == 30 and p[1]==3 and p[2]==3:
        print (p[0])
        raise FoundException
    if p[1] == 3 and p[2] == 3:
        return False
    if p[1] == 0 and p[2] == 0:
        return False
    return True

s = [("22", 0, 0)]

a = [ [ 22 , "-", "9", "*"],
      [ "+",  4 , "-", 18 ],
      [ 4  , "*",  11, "*"],
      [ "*",  8 , "-",  1 ] ]

try:
    for i in range(20):
        s2 = []
        for p, x, y in s:
            for g in gen_possibles(p, x, y):
                if check_prune(g): s2.append(g)
        s = s2.copy()
        print ("now {} possibilities".format(len(s)))
except FoundException:
    pass
