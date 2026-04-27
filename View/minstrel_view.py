import tkinter as tk
from tkinter import ttk
from sys import path
path.insert(0,'../Model')
from minstrel_data import MusicArray,LinkedList

root_color = 'gray25'
root_border_color = 'white'
frame_color = 'gray67'


button_color1 = 'purple2'
button_color2 = 'dodger blue'

label_color = 'gray25'
text_color = 'gray75'




def set_mousewheel(widget, command):
    """Activate / deactivate mousewheel scrolling when 
    cursor is over / not over the widget respectively."""
    widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', command))
    widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

class QueryLevel:
    def __init__(self,root):
        self.query_level = tk.Toplevel(root)
        self.query_level.title('Query')
        self.query_level.geometry('300x300+200+200')
        
        tk.Label(self.query_level,text = 'Search').place(relx = 0.5,
                                                    rely = 0.05,anchor = tk.CENTER)
        
        tk.Label(self.query_level,text = 'Name').place(relx = 0.25,
                                                  rely = 0.1,anchor = tk.CENTER)
        self.name_entry = tk.Entry(self.query_level)
        self.name_entry.place(relx = 0.25,rely = 0.175,anchor = tk.CENTER)

        tk.Label(self.query_level,text = 'Category').place(relx = 0.75,
                                                      rely = 0.1,anchor = tk.CENTER)
        self.category_entry = tk.Entry(self.query_level)
        self.category_entry.place(relx = 0.75,rely = 0.175,anchor = tk.CENTER)

        tk.Label(self.query_level,text = 'Options').place(relx = 0.5,rely = 0.3,
                                                          anchor = tk.CENTER)
        tk.Label(self.query_level,text = 'Search Gate').place(relx = 0.25,rely = 0.4,
                                                     anchor = tk.CENTER)
        self.select_gate = tk.StringVar(self.query_level,value = 'and')
        self.and_radio = tk.Radiobutton(self.query_level,text = 'and',variable = self.select_gate,
                                   value = 'and')
        self.and_radio.place(relx = 0.15,rely = 0.475,anchor = tk.W)
        self.or_radio = tk.Radiobutton(self.query_level,text = 'or',variable = self.select_gate,
                                   value = 'or')
        self.or_radio.place(relx = 0.15,rely = 0.55,anchor = tk.W)
        self.not_radio = tk.Radiobutton(self.query_level,text = 'not',variable = self.select_gate,
                                   value = 'not')
        self.not_radio.place(relx = 0.15,rely = 0.625,anchor = tk.W)

        
        self.search_button = tk.Button(self.query_level,text = 'Search!',width = 10)
                                  #command = query_music)
        self.search_button.place(relx = 0.25,rely = 0.925,anchor = tk.CENTER)

        close_button = tk.Button(self.query_level,text = 'Close',width = 10,
                                  command = self.query_level.destroy)
        close_button.place(relx = 0.75,rely = 0.925,anchor = tk.CENTER)

        
        
class MinstrelView:

    def __init__(self,**kwargs):

        self.root = None

        is_frame = kwargs.get('is_frame',False)
        passed_root = kwargs.get('root',None)

        if is_frame:
            if passed_root == None:
                raise ValueError('Frame provided without a root')
            else:
                self.root = tk.Toplevel(passed_root)
                self.root = passed_root
        else:
            self.root = tk.Tk()

        self.music_array = kwargs.get('music_array',MusicArray())
        self.queue = kwargs.get('queue',LinkedList())

        #Root and Intro Text
        self.root.title('Minstrel')
        self.root.geometry('1200x800+100+100')

        tk.Label(self.root,text = 'Minstrel',
                 font = ('Ariel',20)).place(relx = 0.5,rely = 0.025,anchor = tk.CENTER)

        #Music Frame
        self.music_frame = tk.Frame(self.root,width = 600,height = 250,bg = 'light gray')
        self.music_frame.place(relx = 0.65,rely = 0.7,anchor = tk.CENTER)
        tk.Label(self.music_frame,text = 'Music Goes Here',
                 bg = 'light gray').place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

        self.last_song_window = None 

        #Queue Frame and Canvas
        self.queue_widgets = []
        
        queue_frame_out = tk.Frame(self.root,width = 600,height = 250,bg = 'light gray',
                           highlightbackground = 'black',highlightthickness = 1)
        queue_frame_out.place(relx = 0.65,rely = 0.3,anchor = tk.CENTER)
        tk.Label(queue_frame_out,text = 'Queue Goes Here',
                 bg = 'light gray').place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

        self.queue_canvas = tk.Canvas(queue_frame_out,width = 600,height = 250,
                                     bg = 'white')
        self.queue_canvas.pack(side = tk.TOP,fill = tk.BOTH,expand = 0)

        queue_scroll = ttk.Scrollbar(queue_frame_out,orient = tk.HORIZONTAL,
                                        command = self.queue_canvas.xview)
        queue_scroll.pack(side = tk.BOTTOM,fill = tk.X)

        self.queue_canvas.configure(xscrollcommand = queue_scroll.set)
        self.queue_canvas.bind("<Configure>",lambda e: self.queue_canvas.config(scrollregion = self.queue_canvas.bbox(tk.ALL)))

        #Contains only the scrollable content
        self.queue_frame_in = tk.Frame(self.queue_canvas,width = 300,height = 600,
                                      bg = 'white')
        self.queue_canvas.create_window((0,0),window = self.queue_frame_in,anchor = tk.NW)

        set_mousewheel(self.queue_canvas,lambda e: self.queue_canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        #Queue Option Buttons
        self.clear_button = tk.Button(self.root,text = 'Clear',width = 10)#,command = lambda: fill_queue(clear = True))
        self.clear_button.place(relx = 0.65,rely = 0.5,anchor = tk.CENTER)

        self.next_button = tk.Button(self.root,text = 'Next',width = 10)#,command = next_in_queue)
        self.next_button.place(relx = 0.75,rely = 0.5,anchor = tk.CENTER)

        self.is_repeat = tk.BooleanVar(self.root)
        repeat_check = tk.Checkbutton(self.root,text = 'Repeat',variable = self.is_repeat)
        repeat_check.place(relx = 0.55,rely = 0.5,anchor = tk.CENTER)

        self.is_autoplay = tk.BooleanVar(self.root)
        autoplay_check = tk.Checkbutton(self.root,text = 'Autoplay',variable = self.is_autoplay)
        autoplay_check.place(relx = 0.825,rely = 0.5,anchor = tk.CENTER)

        self.shuffle_button = tk.Button(self.root,text = 'Shuffle',width = 10)#,command = shuffle)
        self.shuffle_button.place(relx = 0.475,rely = 0.5,anchor = tk.CENTER)

        #Query Frame and Canvas
        self.song_widgets = []
        
        selection_frame_out = tk.Frame(self.root,width = 300,height = 600,bg = 'white',
                           highlightbackground = 'black',highlightthickness = 1)
        selection_frame_out.place(relx = 0.2,rely = 0.5,anchor = tk.CENTER)

        self.selection_canvas = tk.Canvas(selection_frame_out,width = 300,height = 600,
                                     bg = 'white')
        self.selection_canvas.pack(side = tk.LEFT,fill = tk.BOTH,expand = 0)

        selection_scroll = ttk.Scrollbar(selection_frame_out,orient = tk.VERTICAL,
                                        command = self.selection_canvas.yview)
        selection_scroll.pack(side = tk.RIGHT,fill = tk.Y)

        self.selection_canvas.configure(yscrollcommand = selection_scroll.set)

        self.selection_canvas.bind("<Configure>",lambda e: self.selection_canvas.config(scrollregion = self.selection_canvas.bbox(tk.ALL)))

        #Contains only the scrollable content
        #You'll have to make the inner frames instance variables so you can access them from the control
        self.selection_frame_in = tk.Frame(self.selection_canvas,width = 300,height = 600,
                                      bg = 'white')
        self.selection_canvas.create_window((0,0),window = self.selection_frame_in,anchor = tk.NW)

        set_mousewheel(self.selection_canvas,lambda e: self.selection_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.query_button = tk.Button(self.root,text = 'Query',width = 10,height = 2)
        self.query_button.place(relx = 0.2,rely = 0.08,anchor = tk.CENTER)

        self.undo_query_button = tk.Button(self.root,text = 'Undo',width = 6)
        self.undo_query_button.place(relx = 0.275,rely = 0.08,anchor = tk.CENTER)

        #All other buttons

        self.newsong_button = tk.Button(self.root,text = 'Add Song',width = 10)#,command = add_new_song)
        self.newsong_button.place(relx = 0.2,rely = 0.9075,anchor = tk.CENTER)

        self.editsong_button = tk.Button(self.root,text = 'Edit Song',width = 10)#command = open_editing_choices)
        self.editsong_button.place(relx = 0.125,rely = 0.9075,anchor = tk.CENTER)

        self.deletesong_button = tk.Button(self.root,text = 'Delete Songs',width = 10)#,command = open_delete)
        self.deletesong_button.place(relx = 0.275,rely = 0.9075,anchor = tk.CENTER)
        
        self.save_button = tk.Button(self.root,text = 'Save',width = 10)#,command = lambda: saving.save_df(music_array.to_df()))
        self.save_button.place(relx = 0.2,rely = 0.95,anchor = tk.CENTER)

        self.quit_button = tk.Button(self.root,text = 'Quit',width = 10,height = 2)#,command = quit_minstrel)
        self.quit_button.place(relx = 0.9,rely = 0.925,anchor = tk.CENTER)

        self.query_level = None
        self.new_song_level = None
        self.select_song_level = None
        self.edit_song_level = None
        self.delete_song_level = None

class NewSongLevel:

    def __init__(self,root):
        self.song_level = tk.Toplevel(root)
        self.song_level.title('Add New Song')
        self.song_level.geometry('750x250+200+600')

        tk.Label(self.song_level,text = '* = Required',font = ('Ariel',8)).place(relx = 0.925,rely = 0.06,anchor = tk.CENTER)

        #Name
        tk.Label(self.song_level,text = 'Name *').place(relx = 0.2,rely = 0.075,anchor = tk.CENTER)
        self.name_entry = tk.Entry(self.song_level)
        self.name_entry.place(relx = 0.2,rely = 0.175,anchor = tk.CENTER)

        #Path
        tk.Label(self.song_level,text = 'Path *').place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)
        self.path_entry = tk.Entry(self.song_level,width = 40)
        self.path_entry.insert(0,'mp3_files/*put your song here*.mp3')
        self.path_entry.place(relx = 0.5,rely = 0.175,anchor = tk.CENTER)

        #Author
        tk.Label(self.song_level,text = 'Author').place(relx = 0.8,rely = 0.075,anchor = tk.CENTER)
        self.author_entry = tk.Entry(self.song_level)
        self.author_entry.place(relx = 0.8,rely = 0.175,anchor = tk.CENTER)

        #Intervals
        tk.Label(self.song_level,text = 'Intervals').place(relx = 0.5,rely = 0.325,anchor = tk.CENTER)
        self.interval_entry = tk.Entry(self.song_level,width = 30)
        self.interval_entry.insert(0,'0.0,')
        self.interval_entry.place(relx = 0.5,rely = 0.425,anchor = tk.CENTER)
        #Checking if user wants intervals every 10 seconds
        self.is_ten = tk.BooleanVar(self.song_level)
        ten_checkbutton = tk.Checkbutton(self.song_level,text = 'Insert Intervals each 20',
                                         variable = self.is_ten)
        ten_checkbutton.place(relx = 0.2,rely = 0.425,anchor = tk.CENTER)

        #Total Time
        tk.Label(self.song_level,text = 'Length(Seconds) *').place(relx = 0.8,rely = 0.325,anchor = tk.CENTER)
        self.total_entry = tk.Entry(self.song_level)
        self.total_entry.insert(0,'60.0')
        self.total_entry.place(relx = 0.8,rely = 0.425,anchor = tk.CENTER)

        #Category
        tk.Label(self.song_level,text = 'Category').place(relx = 0.5,rely = 0.575,anchor = tk.CENTER)
        self.category_entry = tk.Entry(self.song_level)
        self.category_entry.place(relx = 0.5,rely = 0.675,anchor = tk.CENTER)
        
        #Testing Song
        
        self.test_button = tk.Button(self.song_level,text = 'Test Song',width = 10)#command = test_song)
        self.test_button.place(relx = 0.9,rely = 0.85,anchor = tk.CENTER)

        #Adding Song

        self.done_button = tk.Button(self.song_level,text = 'Done',width = 10)#command = add_song)
        self.done_button.place(relx = 0.425,rely = 0.9,anchor = tk.CENTER)

        cancel_button = tk.Button(self.song_level,text = 'Cancel',width = 10,command = self.song_level.destroy)
        cancel_button.place(relx = 0.575,rely = 0.9,anchor = tk.CENTER)

class SelectSongLevel:

    def __init__(self,root,songs):
        self.root = root
        self.choice_level = tk.Toplevel(root)
        self.choice_level.title('Choose a Song')
        self.choice_level.geometry('300x450+200+200')

        tk.Label(self.choice_level,text = 'Choose a Song to Edit').place(relx = 0.5,rely = 0.05,anchor = tk.CENTER)

        #Scrollbar Tomfoolery
        edit_frame_out = tk.Frame(self.choice_level,width = 50,height = 70,bg = 'white',
                               highlightbackground = 'black',highlightthickness = 1)
        edit_frame_out.place(relx = 0.5,rely = 0.45,anchor = tk.CENTER)

        edit_canvas = tk.Canvas(edit_frame_out,width = 200,height = 275,
                                     bg = 'white')
        edit_canvas.pack(side = tk.LEFT,fill = tk.BOTH,expand = 0)

        edit_scroll = ttk.Scrollbar(edit_frame_out,orient = tk.VERTICAL,
                                        command = edit_canvas.yview)
        edit_scroll.pack(side = tk.RIGHT,fill = tk.Y)

        edit_canvas.configure(yscrollcommand = edit_scroll.set)
        edit_canvas.bind("<Configure>",lambda e: edit_canvas.config(scrollregion = edit_canvas.bbox(tk.ALL)))

        #Contains only the scrollable content
        edit_frame_in = tk.Frame(edit_canvas,width = 300,height = 600,
                                      bg = 'white')

        set_mousewheel(edit_canvas,lambda e: edit_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        
        edit_canvas.create_window((0,0),window = edit_frame_in,anchor = tk.NW)

        self.des_song = tk.IntVar(edit_frame_in)

        for i in range(len(songs)):
            rb = tk.Radiobutton(edit_frame_in,text = songs[i].name,
                                variable = self.des_song,value = i)
            rb.grid(row = i,column = 0,pady = 2,sticky = tk.W)

            
        self.select_button = tk.Button(self.choice_level,text = 'Select',width = 10)
                                  #command = bridge_editing)
        self.select_button.place(relx = 0.5,rely = 0.8,anchor = tk.CENTER)

        cancel_button = tk.Button(self.choice_level,text = 'Cancel',width = 10,command = self.choice_level.destroy)
        cancel_button.place(relx = 0.5,rely = 0.9,anchor = tk.CENTER)

        
class EditSongLevel:

    def __init__(self,root,song):
        self.editing_level = tk.Toplevel(root)
        self.editing_level.title(f'Editing {song.name}')
        self.editing_level.geometry('750x250+200+600')

        #Name
        tk.Label(self.editing_level,text = 'Name *').place(relx = 0.2,rely = 0.075,anchor = tk.CENTER)
        self.name_entry = tk.Entry(self.editing_level)
        self.name_entry.insert(0,song.name)
        self.name_entry.place(relx = 0.2,rely = 0.175,anchor = tk.CENTER)

        #Path
        tk.Label(self.editing_level,text = 'Path *').place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)
        self.path_entry = tk.Entry(self.editing_level,width = 40)
        self.path_entry.insert(0,song.path)
        self.path_entry.place(relx = 0.5,rely = 0.175,anchor = tk.CENTER)

        #Author
        tk.Label(self.editing_level,text = 'Author').place(relx = 0.8,rely = 0.075,anchor = tk.CENTER)
        self.author_entry = tk.Entry(self.editing_level)
        self.author_entry.insert(0,song.author)
        self.author_entry.place(relx = 0.8,rely = 0.175,anchor = tk.CENTER)

        #Intervals
        tk.Label(self.editing_level,text = 'Intervals').place(relx = 0.5,rely = 0.325,anchor = tk.CENTER)
        self.interval_entry = tk.Entry(self.editing_level,width = 30)
        self.interval_entry.insert(0,str(song.intervals).replace('[','').replace(']',''))
        self.interval_entry.place(relx = 0.5,rely = 0.425,anchor = tk.CENTER)
        #Checking if user wants intervals every 10 seconds
        self.is_ten = tk.BooleanVar(self.editing_level)
        ten_checkbutton = tk.Checkbutton(self.editing_level,text = 'Insert Intervals each 20',
                                         variable = self.is_ten)
        ten_checkbutton.place(relx = 0.2,rely = 0.425,anchor = tk.CENTER)
        #Total Time
        tk.Label(self.editing_level,text = 'Length(Seconds) *').place(relx = 0.8,rely = 0.325,anchor = tk.CENTER)
        self.total_entry = tk.Entry(self.editing_level)
        self.total_entry.insert(0,song.total_time)
        self.total_entry.place(relx = 0.8,rely = 0.425,anchor = tk.CENTER)

        #Category
        tk.Label(self.editing_level,text = 'Category').place(relx = 0.5,rely = 0.575,anchor = tk.CENTER)
        self.category_entry = tk.Entry(self.editing_level)
        self.category_entry.insert(0,song.category)
        self.category_entry.place(relx = 0.5,rely = 0.675,anchor = tk.CENTER)

        self.done_button = tk.Button(self.editing_level,text = 'Done',width = 10)#,command = write_edits)
        self.done_button.place(relx = 0.4,rely = 0.9,anchor = tk.CENTER)

        cancel_button = tk.Button(self.editing_level,text = 'Cancel',width = 10,command = self.editing_level.destroy)
        cancel_button.place(relx = 0.6,rely = 0.9,anchor = tk.CENTER)

class DeleteSongLevel:

    def __init__(self,root,songs):
        self.del_level = tk.Toplevel(root)
        self.del_level.title('Delete Songs')
        self.del_level.geometry('300x600+200+200')

        tk.Label(self.del_level,text = 'Select Songs to Delete').place(relx = 0.5,rely = 0.05,anchor = tk.CENTER)

        #Scrollbar Tomfoolery
        del_frame_out = tk.Frame(self.del_level,width = 50,height = 100,bg = 'white',
                               highlightbackground = 'black',highlightthickness = 1)
        del_frame_out.place(relx = 0.5,rely = 0.45,anchor = tk.CENTER)

        del_canvas = tk.Canvas(del_frame_out,width = 200,height = 400,
                                     bg = 'white')
        del_canvas.pack(side = tk.LEFT,fill = tk.BOTH,expand = 0)

        del_scroll = ttk.Scrollbar(del_frame_out,orient = tk.VERTICAL,
                                        command = del_canvas.yview)
        del_scroll.pack(side = tk.RIGHT,fill = tk.Y)

        del_canvas.configure(yscrollcommand = del_scroll.set)
        del_canvas.bind("<Configure>",lambda e: del_canvas.config(scrollregion = del_canvas.bbox(tk.ALL)))

        #Contains only the scrollable content
        del_frame_in = tk.Frame(del_canvas,width = 300,height = 600,
                                      bg = 'white')
        del_canvas.create_window((0,0),window = del_frame_in,anchor = tk.NW)

        #These boolvars will determine which songs to delete
        self.boolvars = []
        for i in range(len(songs)):
            self.boolvars.append(tk.BooleanVar(del_frame_in))
        
        for i in range(len(self.boolvars)):
            cb = tk.Checkbutton(del_frame_in,text = songs[i].name,variable = self.boolvars[i],
                                onvalue = True,offvalue = False)
            cb.grid(row = i,column = 0,pady = 2,sticky = tk.W)

        self.toggle_button = tk.Button(self.del_level,text = 'Toggle All',width = 8,height = 2)#,command = toggle_all)
        self.toggle_button.place(relx = 0.5,rely = 0.825,anchor = tk.CENTER)

        self.done_button = tk.Button(self.del_level,text = 'Delete',width = 10)#,command = delete_songs)
        self.done_button.place(relx = 0.8,rely = 0.9,anchor = tk.CENTER)

        cancel_button = tk.Button(self.del_level,text = 'Cancel',width = 10,command = self.del_level.destroy)
        cancel_button.place(relx = 0.8,rely = 0.95,anchor = tk.CENTER)

        
        

if __name__ == '__main__':


    mv = MinstrelView()
    #root = tk.Tk()
    #nsl = NewSongLevel(root)
