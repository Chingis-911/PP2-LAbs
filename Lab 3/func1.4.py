def filter_prime(n):
  if n < 2:
    return False
  if n == 2 or n ==3:
    return True
  if n % 2 == 0 or n % 3 == 0:
    return False
  for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
  return True



x = int(input("Enter lists size : "))
list1  = []

list1 = list(map(int,input("Enter the elements : ").split()))
  

prime_nums = list(filter(lambda num : filter_prime(num), list1))  

print("Prime numbers:", prime_nums)