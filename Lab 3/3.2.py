class Shape:
     def area(self,length = 0):
       length = int(input())
       self.length = length
       print(self.length*self.length)
     class Square():
            def __init__(self,length = 0):
              length = input()
              self.length = length
            def area(self):
               print(self.length*self.length)
 


obj = Shape()
obj.area()