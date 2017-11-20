T = int(raw_input())
for i in range(T):
    Aelement_count  = int(raw_input())
    Aelectments     = raw_input()
    Belement_count  = int(raw_input())
    Belectments     = raw_input()
    
    setA = set(map(int,Aelectments.split()))
    setB = set(map(int,Belectments.split()))
    setCheck = setB.union(setA)
    if (setB == setCheck):
        print "True"
    else:
        print "False"

