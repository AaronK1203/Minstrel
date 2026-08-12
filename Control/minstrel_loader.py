import tkinter as tk
from tkinter import ttk
from minstrel_controller import MinstrelController
import pandas as pd

def set_mousewheel(widget, command):
    """Activate / deactivate mousewheel scrolling when 
    cursor is over / not over the widget respectively."""
    widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
    widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

#Prompts the user to pick a playlist, then creates a MinstrelController
#with the desired playlist
class LoadScreen:
    
    #Creates an instance of class LoadScreen
    def __init__(self):
        
        self.df = pd.read_csv('../Saving/playlists.csv',
                             names = ['name','path'])
        
        
        
        
        #mc = MinstrelController()


#Creates the visuals for a LoadScreen 
class LoadScreenView:

    #Creates an instance of class LoadScreenView
    def __init__(self):
        #Create the root
        self.root = tk.Tk()
        self.root.geometry('450x300+400+400')
        self.root.title('Playlist Selector')

        tk.Label(self.root,
                 text='Select a Playlist to Open',
                 font=('Ariel',10)).place(relx=0.5,rely=0.05,anchor=tk.CENTER)
        
        #Create a scrollable frame
        #Note: file_frame2 is where all the selector button widgets need to go
        
        file_frame = tk.Frame(self.root,width = 150,height = 200,
                      highlightbackground = 'black',highlightthickness = 1)
        file_frame.place(relx = 0.25,rely = 0.5,anchor = tk.CENTER)

        self.file_canvas = tk.Canvas(file_frame,width = 150,height = 200,bg = 'white')
        self.file_canvas.pack(side = tk.LEFT,fill = tk.BOTH,expand = 0)

        file_scrollbar = ttk.Scrollbar(file_frame,orient = tk.VERTICAL,
                                       command = self.file_canvas.yview)
        file_scrollbar.pack(side = tk.RIGHT,fill = tk.Y)

        self.file_canvas.configure(yscrollcommand = file_scrollbar.set)
        self.file_canvas.bind('<Configure>',
                         lambda e: self.file_canvas.config(scrollregion = self.file_canvas.bbox(tk.ALL)))
        self.file_frame2 = tk.Frame(self.file_canvas,width = 200,height = 400,bg = 'white')
        self.file_canvas.create_window((0,0),window = self.file_frame2,anchor = tk.NW)

        set_mousewheel(self.file_canvas,lambda e: self.file_canvas.yview_scroll(int(-1*(e.delta/120)),
                                                                      'units'))
        self.selected_file = tk.IntVar(self.root)
        self.selected_file.set(0)

        tk.Label(self.file_frame2,text='Im a computer').pack()

        #Add Playlist Button
        self.add_playlist_button = tk.Button(self.root,text='Add Playlist',
                                             width=10,height=1)
        self.add_playlist_button.place(relx=0.25,rely = 0.925,anchor=tk.CENTER)

        #Select button
        self.select_button = tk.Button(self.root,text='Open',width=10,
                                       height=2)
        self.select_button.place(relx = 0.75,rely = 0.4,anchor=tk.CENTER)

        #Edit button
        self.edit_button = tk.Button(self.root,text='Edit',width=7,
                                       height=1)
        self.edit_button.place(relx = 0.75,rely = 0.55,anchor=tk.CENTER)

        #Delete button
        self.delete_button = tk.Button(self.root,text='Delete',width=7,
                                       height=1)
        self.delete_button.place(relx = 0.75,rely = 0.675,anchor=tk.CENTER)

        #Cancel button
        self.cancel_button = tk.Button(self.root,text='Quit',width=8,
                                       height=1)
        self.cancel_button.place(relx=0.85,rely=0.9,anchor=tk.CENTER)
        
        
    

if __name__ == '__main__':

    lsv = LoadScreenView()
