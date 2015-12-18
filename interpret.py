import emulate

e = emulate.Emulator()

with open("commands.txt") as f:
    e.stdin = ''.join(f.readlines())

with open("challenge.bin", "rb") as f:
    e.load_bin(f)

try:
    i=0
    while True:
        try:
            e.execute(verbose=True)
            i += 1
        except InputEmptyException:
            s = input ("? ")
            if s == "quit":
                raise emulate.HaltException
            if s == "save":
                with open("state.bin", "wb") as f:
                    e.save_state(f)
            if s == "load":
                with open("state.bin", "rb") as f:
                    e.load_state(f)
                    s = input("=? ")+'\n'
            e.stdin = s+'\n'
            continue

except HaltException:
    with open("trace.txt", "w") as f:
        f.writelines('\n'.join(e.tracelog))
    print("finished: {} instructions".format(i))
    with open("called.txt", "w") as f:
        f.writelines('\n'.join("{}:{}".format(k,v) for k,v in e.call_history.items()))

finally:
    print (e.stdout)