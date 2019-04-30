from tkinter import *
import tkinter as ttk
from tkinter import messagebox
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
import pandas as pd
import random
plotly.offline.init_notebook_mode(connected=True)

# this function is in charge of re plotting the map
def plot(df, q):

    scl = [
        [0, 'rgb(255,255,255)'], # point = 0 for white
        [1, 'rgb(84,39,143)'] # point = 1 for colored 
    ]

    df['text'] = df['code'] + '<br> Hint: ' + df['hint']

    data = dict(type = 'choropleth',
                locations = df['code'],
                locationmode = 'USA-states',
                colorscale = scl,
                text= df['text'],
                z= df['points'].astype(int),
                zmin=0,
                zmax=1,
                showscale=False,
                hoverinfo = 'text') #show just text in hover info

    layout = dict(geo = {'scope':'usa'})

    choromap = go.Figure(data = [data],layout = layout)
    plotly.offline.plot(choromap)


def updatePoints(df, state):
    for index, row in df.iterrows():
        if row['code'] == state:
            df.ix[index, 'points'] = 1
    

def showNextQuestion(curr_question, q):
    i.set(i.get() + 1)
    if i.get() == len(q):
        messagebox.showinfo("End of the game", "Congratulations! You have successfully colored the US.")
    else:
        curr_question.set(q[order[i.get()]])

def submitPressed(df, currentIndex, order, userAnswer, answers, curr_question, questions):

    print(userAnswer)
    print('corect answer ' + answers[currentIndex.get()])
    #if correct, update excel, color map, 
    if (userAnswer == answers[currentIndex.get()]):
        print("correct")
        updatePoints(df, userAnswer)
        showNextQuestion(curr_question, questions)
        plot(df, curr_question)
    else: 
    #if incorrect, try again
        print("incorrect")
        messagebox.showinfo("Error", "Incorrect. Try Again!")

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
#call this everytime you need to update points 
df = pd.read_csv('info.csv')

for col in df.columns:
    df[col] = df[col].astype(str)

# figure.go=Figure(data=data, layout=layout)
# py.plot(figure, filename = 'Color the US')

questions = pd.read_csv('questions.csv')
q = questions['Questions']
a = questions['Answer']

order = [i for i in range(0, len(q))]
#random.shuffle(order)

root = Tk()
root.title("Color the US")
root.configure(bg='aliceblue')

#background

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)
mainframe.configure(bg = 'aliceblue')

lbl = Label(mainframe, text = "Color the US", font = ("Arial Bold",25), bg = 'aliceblue')
lbl.grid(column = 2, row=0)

lbl2 = Label(mainframe, text = "How well do you know your country? ", font = ("Arial", 10), bg = 'aliceblue')
lbl2.grid(column = 2, row = 1)

curr_question = StringVar()

lbl3 = Label(mainframe, textvariable = curr_question, font = ("Arial", 15), bg = 'aliceblue')
lbl3.grid(column = 2, row = 2)

i = IntVar()
i.set(0)
curr_question.set(q[order[i.get()]])

plot(df, i)

#add submit button
button = ttk.Button(root, text ="Submit", command = lambda: submitPressed(df, i, order, tkvar.get(), a, curr_question, q))
button.pack()

# Create a Tkinter variable
tkvar = StringVar(root)

# Dictionary with options
choices = { 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
tkvar.set('AL') # set the default option
# link function to change dropdown
tkvar.trace('w', change_dropdown)

popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose a state", bg = 'aliceblue').grid(column = 2, row = 4, )
popupMenu.grid(column = 2, row = 5)

root.mainloop()