with open("trace.txt", "r") as f:
    trace = [l for l in f.readlines() if "call" in l]

for t in trace:


print (len(trace))