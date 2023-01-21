#!/usr/bin/python3

from tkinter import *
import tkinter as tk
from mipsAssembler import assemble_input , check_labels
from mipsAssembler import *

from tkinter import filedialog
from tkinter import messagebox
 

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

entry1 = tk.Entry (root) 
canvas1.create_window(200, 140, window=entry1)

def getAssembled ():  
    string = entry1.get()
    x1 = assemble_input(string,'1','0',[],[])
    label1 = tk.Label(root, text= x1)
    canvas1.create_window(200, 230, window=label1)
def clicked ():
	file = filedialog.askopenfilename()
	line = '0'
	label = []
	btable = []
	f1 = open('final.obj','a+')
	pc = '0x80001000'
	f = open(file,'r')
	#f2 = open('final.obj')
	fl = f.readlines()
	for string in fl:
		line = check_labels(string,'2',pc,line,label,btable)
		#assemble_input(string)
		line = int(line) + 1
		#print (line)
	for string in fl:
		result = (assemble_input(string,'2',line,label,btable))
		if result not in ['None']:
			f1.write(result)
			f1.write('\n')

	label2 = tk.Label(root, text= 'Succesful: final.obj')
	canvas1.create_window(200, 260, window=label2)

	f.close()
	f1.close()


button1 = tk.Button(text='Enter an instruction', command=getAssembled)
canvas1.create_window(200, 180, window=button1)
button2 = tk.Button(text='Batch Mode', command=clicked)
canvas1.create_window(200, 20, window=button2)
button3 = tk.Button(root, text="Quit", command=root.destroy).pack()
canvas1.create_window(100,20,window=button3)
root.mainloop()
