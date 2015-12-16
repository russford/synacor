s_out = ""
def byte_str(b):
    if b >= 32 and b <= 127:
        return chr(b)
    if b >= 32768:
        return "r%d" % (b-32768)
    return ""

with open("challenge.bin", "rb") as f:
    bytes = f.read()
    code = [bytes[i*2] + (bytes[i*2+1] << 8) for i in range(len(bytes)//2)]


with open("binhex.txt", "w") as f:
    try:
        s=""
        for i,b in enumerate(code):
            if  b==10 or (b>=32 and b<=127):
                s += chr(b)
            f.write("[{:05d}]: {:05d} {}\n".format (i, b, byte_str(b)))
    finally:
        print ([ord(c) for c in s[:20]])
        print (s)

