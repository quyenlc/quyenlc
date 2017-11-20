class MyError(Exception):
    def __str__(self):
        return "n and p should be non-negative"
class Calculator:
    def power(self,n,p):
        if ( (n<0) or (p<0) ):
            raise MyError()
        else:
            return pow(n,p)

myCalculator=Calculator()
T=int(raw_input())
for i in range(T):
    n,p = map(int, raw_input().split())
    try:
        ans=myCalculator.power(n,p)
        print ans
    except Exception,e:
        print e 