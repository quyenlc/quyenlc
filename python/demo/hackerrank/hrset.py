N = int(raw_input())
if ( N%2 == 1 ):
    print "Weird"
elif ( not(N%2) and (N in range(2,6) ) ):
    print "Not Weird"
elif ( not(N%2) and (N in range(6,21)) ):
    print "Weird"
elif ( N>20):
    print "Not Weird"