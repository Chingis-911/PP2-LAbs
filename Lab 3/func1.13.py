import random

x = input("Hello! What is your name? ")
y = int(random.randint(1,20))
cnt = 1
check = 1
txt1 =f"Well,{x}, I am thinking of a number between 1 and 20.\nTake a guess.\n"
guess = int(input(txt1))
while check > 0:
 if guess == y:
    print(f"Good job , {x}! You guessed my number in {cnt} guesses\n")
    check -= check
 elif guess > y:
    guess = int(input("Your guess is too high\nTake a guess.\n"))
    cnt += 1
 else:
    guess = int(input("Your guess is too low!\nTake a guess.\n"))
    cnt += 1

