from tkinter import *
from Result import *



root = Tk()
root.title("Rock Paper Scissor")
root.minsize(width = 750, height = 600)
root.geometry("600x500")


headingFrame1 = Frame(root,bg="#FFBB00",bd=2)
headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)
headingLabel = Label(headingFrame1, text="Welcome to Rock Paper Scissor Game", bg='black', fg='white', font = ('Arial',18))
headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

btn1 = Button(root,text="Rock",bg='White', fg='Black', font=('BritannicBold',30), command =rock)
btn1.place(relx=0.1,rely=0.4, relwidth=0.2,relheight=0.2)

btn2 = Button(root,text="Paper",bg='White', fg='Black', font=('BritannicBold',30), command=paper)
btn2.place(relx=0.4,rely=0.4, relwidth=0.2,relheight=0.2)

btn3 = Button(root,text="Scissor",bg='White', fg='Black', font=('BritannicBold',30), command=scissor)
btn3.place(relx=0.7,rely=0.4, relwidth=0.2,relheight=0.2)

exitBtn  = Button(root,text="Exit",bg='White', fg='Black', font=('BritannicBold',20), command= quit)
exitBtn.place(relx=0.3,rely=0.8, relwidth=0.4,relheight=0.1)

root.mainloop()