import tkinter as tk
import saving
from music import *

def quit_minstrel():
    kill_mixer()
    root.destroy()

root = tk.Tk()
root.title('Minstrel')
root.geometry('1200x800+100+100')
root.protocol('WM_DELETE_WINDOW',quit_minstrel)

tk.Label(root,text = 'Minstrel',
         font = ('Ariel',20)).place(relx = 0.5,rely = 0.025,anchor = tk.CENTER)

#Outer selection frame, contains both the scrollbar and the canvas
selection_frame_out = tk.Frame(root,width = 300,height = 600,bg = 'white',
                           highlightbackground = 'black',highlightthickness = 1)
selection_frame_out.place(relx = 0.2,rely = 0.5,anchor = tk.CENTER)

selection_canvas = tk.Canvas(selection_frame_out,width = 300,height = 600,
                             bg = 'white')
selection_canvas.pack(side = 'left',fill = 'both',expand = True)

selection_scroll = tk.Scrollbar(selection_frame_out,orient = 'vertical',
                                command = selection_canvas.yview)
selection_scroll.pack(side = 'right',fill = 'y')

selection_canvas.configure(yscrollcommand = selection_scroll.set)
selection_canvas.bind('<Configure>',
                      lambda e: selection_canvas.config(scrollregion = selection_canvas.bbox(tk.ALL)))

#Contains only the scrollable content
selection_frame_in = tk.Frame(selection_canvas)
selection_canvas.create_window((0,0),window = selection_frame_in,anchor = 'nw')


for i in range(100):
    tk.Label(selection_frame_in,text = 'Hello').pack()
    
quit_button = tk.Button(root,text = 'Quit',width = 10,height = 2,command = quit_minstrel)
quit_button.place(relx = 0.9,rely = 0.925,anchor = tk.CENTER)


root.mainloop()

