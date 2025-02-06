class Point:
    def getnum(self,first = 0,second = 0):
        first = int(input("Enter the first point:"))
        second = int(input("Enter the second point:"))
        self.first = first
        self.second = second
    
    def show(self):
        txt1 = f"Your first point:{self.first}"
        txt2 = f"Your second point:{self.second}"
        print(txt1)
        print(txt2)    
    def move(self):
        self.first = int(input("Enter new first point:"))
        self.second = int(input("Enter new second point:"))
    def dist(self):
         print(abs(self.first - self.second))
    def act(self):
        op = int(input("Please enter what operation you want to do:\n1.show\n2.move\n3.dist\n"))
        
        if op == 1:
            self.show()
        elif op == 2:
            self.move()
        elif op == 3:
            self.dist()
        else:
            print("No such operatiorns")        

obj = Point()
obj.getnum()
obj.act()       