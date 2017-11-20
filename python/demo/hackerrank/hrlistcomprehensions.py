T= int(raw_input())
results = []
for i in range(T):
    S = raw_input()
    R = S[::-1]
    N = len(S)
    funny = True
    for j in range(1,N):
        if ( abs( ord(S[j]) - ord(S[j-1]) ) != abs( ord(R[j])-ord(R[j-1]) ) ):
            funny = False
    if ( funny ):
        results.append("Funny")
    else:
        results.append("Not Funny")
print "\n".join(results)