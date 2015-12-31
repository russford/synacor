import emulate

e = emulate.Emulator()

with open("commands.txt") as f:
    e.stdin = ''.join(f.readlines())

with open("challenge.bin", "rb") as f:
    e.load_bin(f)

e.print_code_seg(0,6068,"code.txt")

try:
    i=0
    while True:
        i += 1
        if e.stdout and ord(e.stdout[-1]) == 10:
            print (e.stdout, end="")
            e.stdout = ""

        if not e.execute(verbose=True):
            if not e.stdin:
                s = input ("? ")
                if s == "quit":
                    raise emulate.HaltException

                elif s == "save":
                    e.save_state(open("state.bin", "wb"))

                elif s == "load":
                    e.load_state(open("state.bin", "rb"))

                elif s[:5] == "print":
                    addr, func, r2 = map(int, s.strip('\n').split(" ")[1:])
                    n_char = e.code[addr]
                    print (''.join([chr(b^r2) for b in e.code[addr+1:addr+n_char+1]]))

                elif s[:3] == "set":
                    a = s.split(" ")
                    if a[1][0] == "r":
                        e[32768+int(a[1][1:])] = int(a[2])
                    else:
                        e.code[int(a[1])] = int(a[2])

                elif s[:4] == "insp":
                    a = list(map(int, s.split(" ")[1:]))
                    print ("\n".join(["{:>5}: {}".format(i, e.code[i]) for i in range(a[0], a[0]+a[1])]))

                elif s == "reg":
                    print (e.registers)

                else:
                    e.stdin = s+'\n'

except emulate.HaltException:
    # print ("writing files...")
    # with open("trace.txt", "w") as f:
    #     f.writelines('\n'.join(e.tracelog))
    # print("finished: {} instructions".format(i))
    # with open("called.txt", "w") as f:
    #     f.writelines('\n'.join("{}:{}".format(k,v) for k,v in sorted(e.call_history.items())))
    pass

finally:
    print (e.stdout)