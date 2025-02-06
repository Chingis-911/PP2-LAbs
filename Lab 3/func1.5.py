from itertools import permutations
class Farm :
  
  def __init__(self,numheads = ""):
    self.x = numheads

  def getstring(self):
    self.x = str(input("Enter the word : "))
    self.m = list(permutations(self.x))

  def printString(self):
    for p in self.m :
     print(p)


obj = Farm()          # Creates an instance of the class
obj.getstring()      # Calls the method to take user input
obj.printString() 