N = int(raw_input())
s = raw_input()
print sorted(list(set(s.split())),key=int, reverse=True)[1]
