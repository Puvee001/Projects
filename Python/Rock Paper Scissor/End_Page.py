from tkinter import *

root = Tk()
root.title("Result")
root.minsize(width = 400, height = 400)
root.resizable(0,0) # type: ignore
root.geometry("400x400")

def endPage(user,bot,res):
  
    #Customizing result window
    headingFrame = Frame(root,bg="#FFBB18",bd=2)
    headingFrame.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.16)
    headingLabel = Label(headingFrame, text="Thank you for playing !", bg='purple', fg='white', font = ('Arial',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
  
    userFrame = Frame(root,bg="black",bd=2)
    userFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.16)
    userLabel = Label(userFrame, text=user, bg='white', fg='blue', font = ('Rockwell',20))
    ulblLabel = Label(userFrame, text='User chose :', bg='white', fg='black', font = ('Rockwell',20))
    ulblLabel.place(relx=0,rely=0, relwidth=0.5, relheight=1)
    userLabel.place(relx=0.5,rely=0, relwidth=0.5, relheight=1)

    botFrame = Frame(root,bg="black",bd=2)
    botFrame.place(relx=0.1,rely=0.5,relwidth=0.8,relheight=0.16)
    botlblLabel = Label(botFrame, text='Bot Chose :', bg='white', fg='black', font = ('Rockwell',20))
    botLabel = Label(botFrame, text=bot, bg='white', fg='red', font = ('Rockwell',20))
    botlblLabel.place(relx=0,rely=0, relwidth=0.5, relheight=1)
    botLabel.place(relx=0.5,rely=0, relwidth=0.5, relheight=1)
  
    #Customizing background colour
    if res == 'Draw':
            opColor = 'white'
    elif res == 'You win':
            opColor = 'light Green'
    elif res == 'Bot win':
            opColor = 'Orange'
    else:
           opColor = 'white'

    #Result Display
    resultFrame = Frame(root,bg="black",bd=1)
    resultFrame.place(relx=0.1,rely=0.7,relwidth=0.8,relheight=0.16)
    resultLabel = Label(resultFrame, text=res, bg=opColor, fg='black', font = ('Rockwell',20))
    resultLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
