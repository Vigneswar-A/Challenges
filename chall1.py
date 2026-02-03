import random
import secrets

class Panel:
    def __init__(self):
        self.flag_printer = lambda : print("flag{w3lc0m3_h0me_adm1n}")
        self.token_regen() 

    def token_regen(self):
        self.token = secrets.token_hex(16)

    def greet(self):
        name = input("Enter your name: ")
        print(f"Hi {name}, have a good {{0}}".format(random.choice(["day", "night"]), lambda:...))
        return name

    def admin(self):
        self.token_regen()
        if self.token == input("Enter your token: "):
            self.flag_printer()

Panel().greet()
