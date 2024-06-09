from turtle import Turtle

# Font styling
Font = ("Algerian", 20, "normal")
Font1 = ("Chiller", 25, "bold")

class Scoreboard(Turtle):

    def __init__(self):
        self.level = 1
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-280,260)
        self.updateLevel()

# Displaying the level at top
    def updateLevel(self):
        self.clear()
        self.write(f"LEVEL: {self.level}\t"+ "_"*30, align="left", font =Font)

# Updating the level      
    def levelUp(self):
        self.level += 1
        self.updateLevel()

# Displays Game Over message
    def gameOver(self):
        self.goto(0,0)
        self.color("Red")
        self.write(f"GAME OVER!!\n", align="center", font =Font1)
        self.color("Black")       
        self.write(f"Click anywhere to exit", align="center", font =Font)
