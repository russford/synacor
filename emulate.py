from collections import defaultdict

class HaltException(Exception):
    pass

class InputEmptyException(Exception):
    pass

class Emulator(object):
    def __init__(self):
        self.registers = {}
        for i in range(32768, 32776):
            self.registers[i]=0
        self.stack = []
        self.code_ptr = 0
        self.code = []
        self.stdout = ""
        self.stdin = ""
        self.tracelog = []
        self.call_history = defaultdict(int)

    def fetch(self, n):
        if n == 0:
            vals = (0,)
        else:
            vals = tuple(self.code[self.code_ptr+1:self.code_ptr+n+1])
        self.code_ptr += n+1
        return vals

    def __getitem__(self, a):
        if a <= 32767: return a
        elif a < 32776: return self.registers[a]
        else: raise Exception ("out of range %d" % a)

    def __setitem__(self, key, value):
        if key in range(32768, 32776): self.registers[key]=value
        else: raise Exception ("invalid register number %d" % key)

    def halt (self, a):
        raise HaltException

    def _set(self, a):
        self[a[0]] = self[a[1]]

    def push(self, a):
        self.stack.append(self[a[0]])

    def pop(self, a):
        self[a[0]] = self.stack.pop()

    def eq (self, a):
        self[a[0]] = 1 if self[a[1]] == self[a[2]] else 0

    def gt(self, a):
        self[a[0]] = 1 if self[a[1]] > self[a[2]] else 0

    def jmp(self, a):
        self.code_ptr = a[0]

    def jt(self, a):
        if self[a[0]] != 0: self.code_ptr = self[a[1]]

    def jf(self, a):
        if self[a[0]] == 0: self.code_ptr = self[a[1]]

    def add(self, a):
        self[a[0]] = (self[a[1]] + self[a[2]]) % 32768

    def mult(self, a):
        self[a[0]] = (self[a[1]] * self[a[2]]) % 32768

    def mod(self, a):
        self[a[0]] = (self[a[1]] % self[a[2]])

    def _and(self, a):
        self[a[0]] = self[a[1]] & self[a[2]]

    def _or(self, a):
        self[a[0]] = self[a[1]] | self[a[2]]

    def _not(self, a):
        self[a[0]] = (~self[a[1]])&((1<<15)-1)

    def rmem(self, a):
        self[a[0]] = self.code[self[a[1]]]

    def wmem(self, a):
        self.code[self[a[0]]] = self[a[1]]

    def call(self, a):
        if self[a[0]] == 2125:
            self[32768] ^= self[32769]
        elif self[a[0]] == 1531:
            self[32768] ^= self[32770]
            self.stdout += chr(self[32768])
        elif self[a[0]] == 1528:
            self.stdout += chr(self[32768])
        else:
            self.stack.append(self.code_ptr)
            self.code_ptr = self[a[0]]
            self.call_history[self[a[0]]] += 1
    
    def ret(self, a):
        if len(self.stack) == 0:
            raise HaltException
        self.code_ptr = self.stack.pop()
    
    def _out(self, a):
        self.stdout += chr(self[a[0]])
        if chr(self[a[0]]) == '\n': return 1
    
    def _in(self, a):
        if self.stdin == "":
            self.code_ptr -= 2
            return 1
        self[a[0]] = ord(self.stdin[0])
        self.stdout += self.stdin[0]
        self.stdin = self.stdin[1:]


    def noop(self, a):
        pass

    def xor(self, a):
        self[a[0]] = self[a[1]] ^ self[a[2]]


    dispatch = { 0  : (halt, 0),
                 1  : (_set, 2),
                 2  : (push, 1),
                 3  : (pop, 1),
                 4  : (eq, 3),
                 5  : (gt, 3),
                 6  : (jmp, 1),
                 7  : (jt, 2),
                 8  : (jf, 2),
                 9  : (add, 3),
                 10 : (mult, 3),
                 11 : (mod, 3),
                 12 : (_and, 3),
                 13 : (_or, 3),
                 14 : (_not, 2),
                 15 : (rmem, 2),
                 16 : (wmem, 2),
                 17 : (call, 1),
                 18 : (ret, 0),
                 19 : (_out, 1),
                 20 : (_in, 1),
                 21 : (noop, 0),
                 22 : (xor, 1) }

    def c_str(self, p):
        return str(p) if p < 32768 else "r%d" % (p-32768)

    def trace(self, cp=-1):
        if cp == -1: cp = self.code_ptr
        f, n = Emulator.dispatch[self.code[cp]]
        c = ""
        if self.code[cp] == 19:
            c = self[self.code[cp+1]]
            if c == 10:
                c = "(\\n)"
            elif c>=32 and c<=127:
                c = "(%s) " % chr(c)
            else:
                c = "#{:02x} ".format(c)
        elif self.code[cp] == 17:
            c = "@%d" % self.code[cp+1]

        return  "{:>7}: {:<19} r:{} {}".format(
                            "[%d]" % cp,
                            f.__name__.strip("_") + " " + " ".join([self.c_str(p) for p in self.code[cp+1:cp+n+1]]),
                            [self[i] for i in range(32768,32776)],
                            c
                    )

    def execute(self, verbose=False):
        if self.code_ptr > len(self.code):
            raise HaltException
        f, n = Emulator.dispatch[self.code[self.code_ptr]]
        cp = self.code_ptr
        a = self.fetch(n)
        if (verbose):
            self.tracelog.append (self.trace(cp))

        return (f(self,a) != 1)

    def save_state (self, f):
        data = [self.code_ptr] + [self.registers[a] for a in range(32768, 32776)] + [len(self.stack)] + self.stack + self.code
        data = zip([i & ((1<<8)-1) for i in data], [i >> 8 for i in data])
        data = [v for l in data for v in l]
        f.write(bytes(data))

    def load_state (self, f):
        data = f.read()
        data = [data[i*2] + (data[i*2+1] << 8) for i in range(len(data)//2)]
        self.code_ptr = data[0]
        for i in range(32768, 32776):
            self.registers[i] = data[i-32767]
        stacklen = data[9]
        self.stack = data[10:10+stacklen].copy()
        self.code = data[10+stacklen:].copy()
        self.tracelog = []
        self.call_history.clear()

    def load_bin (self, f):
        data = f.read()
        self.code = [data[i*2] + (data[i*2+1] << 8) for i in range(len(data)//2)]
        if len(self.code) < 32768: self.code += [0]*(32768-len(self.code))