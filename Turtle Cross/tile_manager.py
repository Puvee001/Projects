from turtle import Turtle
import random


COLORS = ["violet", "indigo", "blue", "green", "yellow", "orange", "red"]
SHAPES = ["square", "circle", "turtle"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 5


class tileManager:
    def __init__(self):
        self.all_tiles = []
        self.tile_speed = STARTING_MOVE_DISTANCE

# Creating Random tiles at random positions
    def create_tiles(self):
        chance = random.randint(1,6)
        if chance == 1:
            new_tiles = Turtle(random.choice(SHAPES))
            new_tiles.shapesize(stretch_wid = 1.5, stretch_len = 2)
            new_tiles.penup()
            new_tiles.color(random.choice(COLORS))
            random_y = random.randint(-270, 270)
            new_tiles.goto(-300,random_y)
            self.all_tiles.append(new_tiles)

# Making tiles move
    def move_tiles(self):
        for tile in self.all_tiles:
            tile.forward(self.tile_speed)

# Increasing speed
    def levelUp(self):
        self.tile_speed += MOVE_INCREMENT
