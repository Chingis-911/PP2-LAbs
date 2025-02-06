class Bank:
    def __init__(self,name = "",deposit = 0):
        name = str(input("Enter yoyr name:"))
        deposit = int(input("Enter amount of money:"))
        self.name = name
        self.depository = deposit
    def deposit(self,plus = 0):
        plus = int(input("Enter amount of money: "))
        self.depository += plus
        txt1 = f"Your current depository is {self.depository}" 
        print(txt1)
    def withdraw(self,minus = 0):
        minus = int(input("Enter amount of money: "))
        if minus > self.depository:
            print("Not enough money bro")
        else:
         self.depository -= minus
         txt2= f"Your current depository is {self.depository}" 
         print(txt2)
    def act(self):
        op = int(input("Please enter what operation you want to do:\n1.deposit\n2.withdraw\n"))
        
        if op == 1:
           self.deposit()
        elif op == 2:
            self.withdraw()
        else:
            print("No such operatiorns")        

obj = Bank()
obj.act()       