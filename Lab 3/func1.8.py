x = int(input("Enter lists size : "))

list1 = list(map(int,input("Enter the elements : ").split()))
cnt = 0
for i in range(len(list1) - 2) :
 if list1[i] == 0 and  list1[i + 1] == 0 and list1[i + 2] == 7:
  cnt += 1 
 


if cnt == 1:
 print("True")
else:
 print("False")
 