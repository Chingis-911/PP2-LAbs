x = (input("Enter your word: "))
cnt = 0
if len(x) > 0:
    for i in range(len(x)//2):
      if x[i] == x[len(x) - 1 - i]:
         cnt += 1
if x == x[::-1]:
   print("is palindrome")
else:
   print("not palindrome")   


if cnt == len(x)//2:
    print("is palyndrome")
else:
 print("not palyndrome")            

               