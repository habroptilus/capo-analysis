chords = []
N = 40000
for i in range(N):
    L = input().split(" ")
    L.pop()
    for i in L:
        if i not in chords:
            chords.append(i)
print(" ".join(chords))
print(len(chords))
