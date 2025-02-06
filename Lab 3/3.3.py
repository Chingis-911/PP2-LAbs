class Rectangle:
     def area(self,length = 0,width = 0):
       length = int(input("Type length:"))
       width = int(input("Type width:"))
       self.length = length
       self.width = width
       txt = f"{self.length*self.width} cm^2"
       print(txt) 
      


obj = Rectangle()
obj.area()