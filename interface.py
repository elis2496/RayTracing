import os
import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from PIL import Image, ImageTk

from utils import make_3Dimage


root = Tk()  #create main window
root.title("RayTracing")
        
def read_fpath_w_h(event, filename, s_filename):
    """The function takes a certain event - the user pressing a button"""
    try:
        filename = entry_file.get()
        w = int(entry_width.get())
        h = int(entry_height.get())
        if os.path.isfile(filename) and h > 0 and w > 0:
            message_label["text"] = "ok"
            make_3Dimage(filename, w, h, s_filename)
            tk = Toplevel() 
            c = Canvas(tk, width=w, height=h)
            src_img = Image.open(s_filename)
            img = ImageTk.PhotoImage(src_img)
            c.create_image(0, 0, image=img, anchor="nw")
            c.pack(fill=BOTH)
            Label(tk, text=filename).pack(fill=BOTH)
            tk.mainloop()
        else:
            message_label["text"]="Enter correct values"
    except ValueError:
        message_label["text"] = "Enter correct value"
        

start_work = Label(root, text=" Enter values:",font=15)
message_label = Label(root,width=27, font=15)

file = Label(root, text="File",font=15)
entry_file = Entry(root, width=20, font=15)


width = Label(root, text="Width",font=15)
entry_width = Entry(root, width=3, font=15)


height = Label(root, text="Height",font=15)
entry_height = Entry(root, width=3, font=15)


button_enter = Button(root, text="Enter")

start_work.grid()
file.grid(row=1, column=0,sticky=E)
entry_file.grid(row=1, column=1)
width.grid(row=2, column=0,sticky=E)
entry_width.grid(row=2, column=1)
height.grid(row=3, column=0,sticky=E)
entry_height.grid(row=3, column=1)
button_enter.grid(row=4, column=1)
message_label.grid(row=5, column=1)
button_enter.bind("<Button-1>",read_fpath_w_h)
root.mainloop()