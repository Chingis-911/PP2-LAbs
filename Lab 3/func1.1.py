class Shop :
  def __init__(self,gr = 0):
    self.name = gr

  def getstring(self):
    self.name = int(input("Enter amount of gr : "))

  def printString(self):
    print(28.3495231*self.name)

obj = Shop()          # Creates an instance of the class
obj.getstring()      # Calls the method to take user input
obj.printString() 