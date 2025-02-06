class Wer :
  def __init__(self,name="Anon"):
    self.name = name

  def getstring(self):
    self.name = input()

  def printString(self):
    print(self.name.upper())

obj = Wer()          # Creates an instance of the class
obj.getstring()      # Calls the method to take user input
obj.printString()    # Calls the method to print the uppercase version