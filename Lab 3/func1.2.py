class Convert :
  def __init__(self,gr = 0):
    self.name = gr

  def getstring(self):
    self.name = int(input("Enter the farengeit tempreature : "))

  def printString(self,a = 0):
    a = 5/9
    print(a*(self.name - 32))

obj = Convert()          # Creates an instance of the class
obj.getstring()      # Calls the method to take user input
obj.printString() 