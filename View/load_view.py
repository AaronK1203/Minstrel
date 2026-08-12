import tkinter as tk
from tkinter import ttk

def set_mousewheel(widget, command):
    """Activate / deactivate mousewheel scrolling when 
    cursor is over / not over the widget respectively."""
    widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
    widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

#Creates the visuals for a LoadScreen 
class LoadScreenView:

    #Creates an instance of class LoadScreenView
    def __init__(self):

        #Extra window variables to implement singleton
        self.add_playlist_level = None
        self.edit_playlist_level = None
        self.delete_playlist_level = None
        
        #Create the root
        self.root = tk.Tk()
        self.root.geometry('450x300+400+400')
        self.root.title('Playlist Selector')
        
        #Stores radiobuttons related to which playlist is selected
        #(Allows for the erasure of radiobuttons for when the frame
        #needs to be reloaded)
        self.frame_widgets = []

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

        #Quit button
        self.quit_button = tk.Button(self.root,text='Quit',width=8,
                                       height=1)
        self.quit_button.place(relx=0.85,rely=0.9,anchor=tk.CENTER)


    #Fills the scrollable frame with radiobuttons given a list of values
    def fill_selection_frame(self,names):
        #Empties the frame (does nothing if no buttons generated
        for i in range(len(self.frame_widgets)):
            self.frame_widgets[i].destroy()
        self.frame_widgets.clear()

        #Fills the frame, one radiobutton per attribute

        for i in range(len(names)):
            self.frame_widgets.append(tk.Radiobutton(self.file_frame2,text=names[i],width = 15,
                                                         height = 2,indicator = 0,
                                                         variable = self.selected_file,
                                                         value = i))
            self.frame_widgets[i].grid(row = i,column = 0,padx = 1,pady = 1)

        self.file_canvas.configure(scrollregion = self.file_canvas.bbox(tk.ALL))

#Creates window for adding playlists
class AddPlaylistView:

    #Creates the instance of the AddPlaylist View
    def __init__(self,root):

        self.newplay_level = tk.Toplevel(root)
        self.newplay_level.title('New Playlist')
        self.newplay_level.geometry('300x150+500+200')

        tk.Label(self.newplay_level,text = 'Name').place(relx = 0.25,
                                                         rely = 0.15,anchor = tk.CENTER)

        self.name_entry = tk.Entry(self.newplay_level)
        self.name_entry.place(relx = 0.25,rely = 0.3,anchor = tk.CENTER)

        tk.Label(self.newplay_level,text = 'Directory').place(relx = 0.75,
                                                         rely = 0.15,anchor = tk.CENTER)

        self.directory_entry = tk.Entry(self.newplay_level)
        self.directory_entry.place(relx = 0.75,rely = 0.3,anchor = tk.CENTER)
        self.directory_entry.insert(0,'Your-Playlist.csv')
        
        self.do_auto_generate = tk.BooleanVar(self.newplay_level)
        self.do_auto_generate.set(True)
        genname_checkbutton = tk.Checkbutton(self.newplay_level,
                                             text = 'Generate Directory with Name',
                                             variable = self.do_auto_generate)
        genname_checkbutton.place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

        self.create_button = tk.Button(self.newplay_level,text = 'Create',width = 18)
                                  #command = create_file)
        self.create_button.place(relx = 0.25,rely = 0.9,anchor = tk.CENTER)

        cancel_button = tk.Button(self.newplay_level,text = 'Cancel',width = 18,
                                  command = self.newplay_level.destroy)
        cancel_button.place(relx = 0.75,rely = 0.9,anchor = tk.CENTER)

#Creates window for editing playlists
class EditPlaylistView:

    #Creates the instance of the EditPlaylist View
    def __init__(self,root,file):

        self.editplay_level = tk.Toplevel(root)
        self.editplay_level.title('Edit Playlist')
        self.editplay_level.geometry('300x150+500+200')

        tk.Label(self.editplay_level,text = 'Name').place(relx = 0.25,
                                                         rely = 0.15,anchor = tk.CENTER)

        self.name_entry = tk.Entry(self.editplay_level)
        self.name_entry.place(relx = 0.25,rely = 0.3,anchor = tk.CENTER)
        self.name_entry.insert(0,file[0])

        tk.Label(self.editplay_level,text = 'Directory').place(relx = 0.75,
                                                         rely = 0.15,anchor = tk.CENTER)

        self.directory_entry = tk.Entry(self.editplay_level)
        self.directory_entry.place(relx = 0.75,rely = 0.3,anchor = tk.CENTER)
        self.directory_entry.insert(0,file[1])
        
        self.do_auto_generate = tk.BooleanVar(self.editplay_level)
        self.do_auto_generate.set(True)
        genname_checkbutton = tk.Checkbutton(self.editplay_level,
                                             text = 'Generate Directory with Name',
                                             variable = self.do_auto_generate)
        genname_checkbutton.place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

        self.set_button = tk.Button(self.editplay_level,text = 'Set',width = 18)
                                  #command = create_file)
        self.set_button.place(relx = 0.25,rely = 0.9,anchor = tk.CENTER)

        cancel_button = tk.Button(self.editplay_level,text = 'Cancel',width = 18,
                                  command = self.editplay_level.destroy)
        cancel_button.place(relx = 0.75,rely = 0.9,anchor = tk.CENTER)

#Creates window for deleting playlist
class DeletePlaylistView:
    #Creates an instance of DeletePlaylistView
    #param file is a tuple obtained by taking the row of the index specified
    #by the radiobutton
    def __init__(self,root,file):
        self.file_index = 0

        self.check_level = tk.Toplevel(root)
        tk.Label(self.check_level,text = f'Delete {file[1]}',font = ('Ariel',12)).pack()
        tk.Label(self.check_level,text = f'Are You Sure?').pack()
        tk.Label(self.check_level,text = f'(This Action Cannot be Undone)').pack()

        self.delete_button = tk.Button(self.check_level,text = 'Delete',width = 8)
        self.delete_button.pack()

        cancel_button = tk.Button(self.check_level,text = 'Cancel',width = 12,height = 2,
                                  command = self.check_level.destroy)
        cancel_button.pack(pady = 2)
    
#Used to display errors to the user
class ErrorLevel:

    #Creates an ErrorLevel instance
    def __init__(self,root,message):
        self.error_level = tk.Toplevel(root)
        self.error_level.title('Error')
        self.error_level.geometry('250x100+500+500')

        tk.Label(self.error_level,text=message,font=('Ariel',10)).place(relx = 0.5,rely = 0.35,anchor = tk.CENTER)
        tk.Button(self.error_level,text='Close',width=10,
                  command = self.error_level.destroy).place(relx = 0.5,rely = 0.8,anchor = tk.CENTER)


if __name__ == '__main__':

    lsv = LoadScreenView()
    lsv.fill_selection_frame(['Hello','im','a','computer'])

    #err = ErrorLevel(lsv.root,'I am an error')
    delete = DeletePlaylistView(lsv.root,['hello','hi.csv'])

