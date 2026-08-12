from sys import path
import pandas as pd

path.insert(0,'../Model')
path.insert(0,'../View')

from load_data import *
from load_view import *
from minstrel_controller import *

def bind_button(button,command):
    button.configure(command = command)

#Links the LoadScreenModel and LoadScreenView classes to form the application
class LoadScreenController:

    def __init__(self):
        self.view = LoadScreenView()
        self.model = LoadScreenModel()

        #Add the radiobuttons to the view
        self.update_selection_frame()

        #Pair Quit Button with quit()
        bind_button(self.view.quit_button,self.quit)

        #Pair Open button with open_file()
        bind_button(self.view.select_button,self.open_file)

        #Pair Add button with create_add_window()
        bind_button(self.view.add_playlist_button,self.create_add_window)

        #Pair edit button with create_edit_window()
        bind_button(self.view.edit_button,self.create_edit_window)
        
        #Pair delete button with create_delete_window()
        bind_button(self.view.delete_button,self.create_delete_window)

        #Bind the quit method to the x button
        self.view.root.protocol('WM_DELETE_WINDOW',self.quit)


        self.view.root.mainloop()
        

    #Updates the selection frame with the names in the models df
    def update_selection_frame(self):
        names = self.model.df['name'].tolist()
        self.view.fill_selection_frame(names)

    #Opens the file specified by the view's radiobuttons
    def open_file(self):
        file_index = self.view.selected_file.get()
        save_file = self.model.df.iat[file_index,1]
        self.minstrel_control = MinstrelController(save_file=save_file)

    #Stops the application
    def quit(self):
        #Save info
        self.model.df_to_save(self.model.df)
        #Destroy self
        self.view.root.destroy()

    '''Add Playlist Methods'''
    
    #Opens the add window
    def create_add_window(self):
        #singleton
        if self.view.add_playlist_level != None and self.view.add_playlist_level.newplay_level.winfo_exists():
            self.view.add_playlist_level.newplay_level.lift()
            return
    
        self.view.add_playlist_level = AddPlaylistView(self.view.root)
        add_level = self.view.add_playlist_level

        #Bind buttons
        bind_button(add_level.create_button,self.add_playlist)

        add_level.newplay_level.mainloop()

    #Given the user's inputs in entries, creates new csv file
    def add_playlist(self):
        add_level = self.view.add_playlist_level
        name = add_level.name_entry.get()
        path = add_level.directory_entry.get()

        #If the user requests to auto-generate the name,
        #take the name and replace the spaces with dashes, then add csv
        if add_level.do_auto_generate.get():
            temp = name.replace(' ','-')
            path = f'{temp}.csv'

        #Check for errors

        #Path does not end in .csv
        if path[len(path)-4:len(path)] != '.csv':
            path += '.csv'
        
        #Name is empty
        if name == '':
            e = ErrorLevel(add_level.newplay_level,'Error: Name Cannot be Empty')
            return

        #Path < 5 chars
        if len(path) < 5:
            e = ErrorLevel(add_level.newplay_level,'Error: Path is too short')
            return
        
        #Name already exists
        if name in self.model.df['name'].tolist():
            e = ErrorLevel(add_level.newplay_level,'Error: Name Already Exists')
            return

        #Path already exists
        if path in self.model.df['path'].tolist():
            e = ErrorLevel(add_level.newplay_level,'Error: Name Already Exists')
            return
        
        #Make the file and add it to the df
        self.model.create_csv(name,path)
        self.update_selection_frame()
        add_level.newplay_level.destroy()
        
    '''Edit Playlist Methods'''

    #creates edit window given the current intvar value
    def create_edit_window(self):
        #singleton
        if self.view.edit_playlist_level != None and self.view.edit_playlist_level.editplay_level.winfo_exists():
            self.view.edit_playlist_level.editplay_level.lift()
            return
        #Get information to fill edit window
        file_index = self.view.selected_file.get()
        name = self.model.df.iloc[file_index,0]
        path = self.model.df.iloc[file_index,1]
        
        #Open edit window
        self.view.edit_playlist_level = EditPlaylistView(self.view.root,[name,path])
        edit_level = self.view.edit_playlist_level

        #Bind buttons and methods

        bind_button(self.view.edit_playlist_level.set_button,lambda: self.edit_playlist(file_index))

        edit_level.editplay_level.mainloop()

    def edit_playlist(self,index):
        edit_level = self.view.edit_playlist_level
        name = edit_level.name_entry.get()
        path = edit_level.directory_entry.get()

        #If the user requests to auto-generate the name,
        #take the name and replace the spaces with dashes, then add csv
        if edit_level.do_auto_generate.get():
            temp = name.replace(' ','-')
            path = f'{temp}.csv'

        #Check for errors

        #Path does not end in .csv
        if path[len(path)-4:len(path)] != '.csv':
            path += '.csv'
        
        #Name is empty
        if name == '':
            e = ErrorLevel(edit_level.editplay_level,'Error: Name Cannot be Empty')
            return

        #Path < 5 chars
        if len(path) < 5:
            e = ErrorLevel(edit_level.editplay_level,'Error: Path is too short')
            return
        
        #Name already exists
        matching_index = self.model.df.index[self.model.df['name'] == name].tolist()
        if name in self.model.df['name'].tolist() and matching_index[0] != index:
            e = ErrorLevel(edit_level.editplay_level,'Error: Name Already Exists')
            return

        #Path already exists
        matching_index = self.model.df.index[self.model.df['path'] == path].tolist()
        if path in self.model.df['path'].tolist() and matching_index[0] != index:
            e = ErrorLevel(edit_level.editplay_level,'Error: Path Already Exists')
            return

        #Edit the path
        self.model.edit_csv(index,name,path)
        self.update_selection_frame()
        edit_level.editplay_level.destroy()
        

    '''Delete Playlist Methods'''
    #Creates the window for deleting a file
    def create_delete_window(self):
        #singleton
        if self.view.delete_playlist_level != None and self.view.delete_playlist_level.check_level.winfo_exists():
            self.view.delete_playlist_level.check_level.lift()
            return

        #Get information to fill delete window
        file_index = self.view.selected_file.get()
        name = self.model.df.iloc[file_index,0]
        path = self.model.df.iloc[file_index,1]
        
        #Open delete window
        self.view.delete_playlist_level = DeletePlaylistView(self.view.root,[name,path])
        delete_level = self.view.delete_playlist_level

        #Pair buttons
        bind_button(self.view.delete_playlist_level.delete_button,lambda: self.delete_file(file_index))

        delete_level.check_level.mainloop()

    #Deletes the file
    def delete_file(self,index):
        self.model.delete_csv(index)
        self.update_selection_frame()
        self.view.delete_playlist_level.check_level.destroy()
        

if __name__ == '__main__':

    c = LoadScreenController()

        
    
    
