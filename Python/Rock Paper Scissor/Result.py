from tkinter import *
import random
from tkinter import messagebox
from End_Page import *


def result(choice):
    bot_choice = random.choice(['scissor','rock','paper'])
    #Evaluvating result
    if (choice == bot_choice):
        #messagebox.showwarning(title='The match has ended' , message= f'Your choice : {choice} \n bot choice : {bot_choice} \n The match is draw :|')
        endPage(choice,bot_choice,'Draw')
    elif (choice == 'scissor' and bot_choice == 'paper') or (choice == 'paper' and bot_choice == 'rock') or (choice == 'rock' and bot_choice == 'scissor'):
        #messagebox.showinfo(title='The match has ended' , message= f'Your choice : {choice} \n bot choice : {bot_choice} \n You won the match :)')
        endPage(choice,bot_choice,'You win')
    elif (bot_choice == 'scissor' and choice == 'paper') or (bot_choice == 'paper' and choice == 'rock') or (bot_choice == 'rock' and choice == 'scissor'):
        #messagebox.showerror(title='The match has ended' , message= f'Your choice : {choice} \n bot choice : {bot_choice} \n Bot won the match :(')
        endPage(choice,bot_choice,'Bot win')
    else:
        return
    

def rock():
    result('rock')

def scissor():
    result('scissor')
  
def paper():
    result('paper')
