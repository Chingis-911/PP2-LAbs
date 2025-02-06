x = int(input("Enter lists size : "))

list1 = list(map(int,input("Enter the elements : ").split()))
list2 = []

list1.sort()
print(list1)
for i in range(len(list1)) :
 if len(list2) == 0:
  list2.append(list1[i])
 if len(list2) != 0 and list2[len(list2) - 1] != list1[i]:
  list2.append(list1[i])
 else:
  continue
 
print(list2)
 