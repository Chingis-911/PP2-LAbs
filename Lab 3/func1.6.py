class Rev :
    def getsent(self,x = ""):
        x = str(input("Enter your sentence : "))
        self.c = x

    def reversia(self):
        self.reve =" ".join(self.c.split()[::-1])
        print(self.reve)
        print(self.c[::-1])

obj = Rev()
obj.getsent()
obj.reversia()