import emulate

e = emulate.Emulator()

with open("commands.txt") as f:
    e.stdin = ''.join(f.readlines())

with open("challenge.bin", "rb") as f:
    e.load_bin(f)

try:
    i=0
    while True:
        i += 1
        if not e.execute(verbose=True):
            if e.stdout:
                print (e.stdout, end="")
                e.stdout = ""
            if not e.stdin:
                s = input ("? ")
                if s == "quit":
                    raise emulate.HaltException
                elif s == "save":
                    with open("state.bin", "wb") as f:
                        e.save_state(f)
                elif s == "load":
                    with open("state.bin", "rb") as f:
                        e.load_state(f)
                else:
                    e.stdin = s+'\n'

except emulate.HaltException:
    print ("writing files...")
    with open("trace.txt", "w") as f:
        f.writelines('\n'.join(e.tracelog))
    print("finished: {} instructions".format(i))
    with open("called.txt", "w") as f:
        f.writelines('\n'.join("{}:{}".format(k,v) for k,v in e.call_history.items()))

finally:
    print (e.stdout)