from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 15
FINISH_LINE_Y = 280


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)

# Movement controls        
    def go_up(self):
        self.forward(MOVE_DISTANCE)
    def go_down(self):
        self.backward(MOVE_DISTANCE)

# Prevents Out of the screen
    def checkPosition(self):
        if (self.ycor() < -280):
            return True
        else:
            return False

# Screen refresh for new level            
    def reset(self):
        self.goto(STARTING_POSITION)

# checking for reaching finish line        
    def is_finished(self):
        if (self.ycor() > FINISH_LINE_Y):
            return True
        else:
            return False
