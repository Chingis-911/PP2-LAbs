class Farm :
  def __init__(self,numheads = 0,numlegs = 0):
    self.x = numheads
    self.y = numlegs

  def getstring(self):
    self.x = int(input("Enter amount of heads : "))
    self.y = int(input("Enter amount of legs : "))
    self.b = self.x * 4
    self.c = self.b - self.y
    self.chick = self.c / 2
    self.rabb = self.x - self.chick 

  def printString(self) :
    txt = f"Number of chickens : {self.chick}\nNumber of rabbits : {self.rabb} "
    print(txt)




obj = Farm()          # Creates an instance of the class
obj.getstring()      # Calls the method to take user input
obj.printString() 