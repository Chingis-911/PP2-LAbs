
x = int(input("Enter lists size : "))

list1 = list(map(int,input("Enter the elements : ").split()))
c = False
cnt = 0
for i in range(len(list1) - 1) :
 if list1[i] == 3 and list1[i] == list1[i + 1]:
  cnt += 1 
 


if cnt == 1:
 print("True")
else:
 print("False")
 

