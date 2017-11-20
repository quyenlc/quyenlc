def checkPalindromic( number ):
	if number < 0:
		reverse_number = -1 * int(''.join(reversed(str(number)[1:])))
	else:
		reverse_number = int(''.join(str(number)[::-1]))
	if number == reverse_number:
		return True
	else:
		return False
def checkPositive( numbers ):
	return all(list(map(lambda x: x >0,numbers)));
N= int(input())
numbers = map(int,raw_input().split())
print (all([checkPositive(numbers), any(list(map(checkPalindromic,numbers)))]))