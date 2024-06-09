import time
from turtle import Screen
from player import Player
from tile_manager import tileManager
from scoreboard import Scoreboard
from tkinter import messagebox

screen = Screen()
screen.setup(width = 600, height = 600)
screen.tracer (0)

#Calling all clases
player = Player()
tile_manager = tileManager()
Scoreboard = Scoreboard()

#Setting up the screem
screen.listen()
screen.title("Turtle & Tiles")
messagebox.showinfo(message = "Use up and down arrows to move")

#Moving the turtle
screen.onkey(player.go_up, "Up")
screen.onkey(player.go_down, "Down")

#Seting up the game
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    tile_manager.create_tiles()
    tile_manager.move_tiles()


    if player.checkPosition():
        player.reset()

    #Setting Game over message
    for tile in tile_manager.all_tiles:
        if tile.distance(player) < 20:
            game_is_on = False
            Scoreboard.gameOver()
            
    #Finishing the level
    if player.is_finished():
        player.reset()
        tile_manager.levelUp()
        Scoreboard.levelUp()

screen.exitonclick()


