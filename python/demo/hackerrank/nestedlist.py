N =int(raw_input())
records = []
myset =set()
for i in range(0,N):
    name = raw_input()
    grade = float(raw_input())
    record = [name,grade]
    myset.add(grade)
    records.append(record)
records.sort(key=lambda x: x[1])
secondlowestgrade = float(sorted(list(myset))[1])
for i in records:
    if (i[1] == secondlowestgrade) :
        print i[0]