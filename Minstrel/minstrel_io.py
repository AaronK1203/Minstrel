import tkinter as tk
from tkinter import ttk
import saving
from minstrel_clock import Clock
from saving import Node
from saving import Linked_List
from saving import Music_Array
from music import *
from pathlib import Path
import random

'''Beginning of Importing Save Data and Parsing'''
music_array = saving.save_to_music_array()
queue = Linked_List()


global last_song_window

#Note: This variable has to be mutable, so I made it an array with one object. Lord, forgive me.
last_song_window = [None]

'''End of Importing Save Data and Parsing'''

def quit_minstrel():
    kill_mixer()
    root.destroy()


root = tk.Tk()
root.title('Minstrel')
root.geometry('1200x800+100+100')
root.protocol('WM_DELETE_WINDOW',quit_minstrel)

tk.Label(root,text = 'Minstrel',
         font = ('Ariel',20)).place(relx = 0.5,rely = 0.025,anchor = tk.CENTER)


'''Beginning of Queue Frame and Canvas'''
#Frame for Storing the queue
queue_frame_out = tk.Frame(root,width = 600,height = 250,bg = 'light gray',
                           highlightbackground = 'black',highlightthickness = 1)
queue_frame_out.place(relx = 0.65,rely = 0.3,anchor = tk.CENTER)
tk.Label(queue_frame_out,text = 'Queue Goes Here',
         bg = 'light gray').place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

queue_canvas = tk.Canvas(queue_frame_out,width = 600,height = 250,
                             bg = 'white')
queue_canvas.pack(side = tk.TOP,fill = tk.BOTH,expand = 0)

queue_scroll = ttk.Scrollbar(queue_frame_out,orient = tk.HORIZONTAL,
                                command = queue_canvas.xview)
queue_scroll.pack(side = tk.BOTTOM,fill = tk.X)

queue_canvas.configure(xscrollcommand = queue_scroll.set)
queue_canvas.bind("<Configure>",lambda e: queue_canvas.config(scrollregion = queue_canvas.bbox(tk.ALL)))

#Contains only the scrollable content
queue_frame_in = tk.Frame(queue_canvas,width = 300,height = 600,
                              bg = 'white')
queue_canvas.create_window((0,0),window = queue_frame_in,anchor = tk.NW)

queue_widgets = []

def fill_queue(**kwargs):

    #Skips to node of param skips
    def go_to_node(skips):
        n = queue.head
        for i in range(skips):
            n = n.next
        queue.head = n
        if last_song_window != [None]:
            last_song_window[0].destroy()
        last_song_window[0] = queue.head.song.to_canvas(music_frame)
        last_song_window[0].place(relx = 0.5, rely = 0.5,anchor = tk.CENTER)
        queue.head.song.load()
        fill_queue()
        
    #Resets the queue to a blank linked list
    is_clear = kwargs.get('clear',False)
    if bool(is_clear):
        queue.head = None
        
    #Clear the Queue frame to make way for new widgets
    for i in range(len(queue_widgets)):
        queue_widgets[i].destroy()

    queue_widgets.clear()
    
    #If the queue is empty, do nothing
    if queue.head == None:
        queue_widgets.append(tk.Label(queue_canvas,text = 'Queue Empty'))
        queue_widgets[0].place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)
        return
    #Note: There is a problem with the scrollbar not adjusting correctly for the first iteration
    #Considering that the user will not need to scroll until a couple of songs have been added to the queue
    #This issue doesn't mean much (Knock on wood)

    n = queue.head
    i = 0
    while n != None:
        queue_widgets.append(tk.Button(queue_frame_in,text = n.song.name,command = lambda i=i:go_to_node(i)))
        queue_widgets[i].grid(row = 0,column = i,padx = 10,pady = 30)
        
        n = n.next
        i+=1
    #To fix the scrollbar not reaching all the widgets        (Wow that's a lot of spaces)
    corrector = tk.Label(queue_frame_in,text = '                                                          ',bg = 'white')
    queue_widgets.append(corrector)
    corrector.grid(row = 0,column = i+1,padx = 10)
    
    
    queue_canvas.configure(scrollregion = queue_canvas.bbox(tk.ALL))
        
fill_queue()

def next_in_queue():
    #If either head or head.next is null, do nothing
    if queue.head == None or queue.head.next == None:
        return
    queue.head = queue.head.next

    if last_song_window != [None]:
        last_song_window[0].destroy()
    last_song_window[0] = queue.head.song.to_canvas(music_frame)
    last_song_window[0].place(relx = 0.5, rely = 0.5,anchor = tk.CENTER)
    queue.head.song.load()
    fill_queue()
    

clear_button = tk.Button(root,text = 'Clear',width = 10,command = lambda: fill_queue(clear = True))
clear_button.place(relx = 0.65,rely = 0.5,anchor = tk.CENTER)

next_button = tk.Button(root,text = 'Next',width = 10,command = next_in_queue)
next_button.place(relx = 0.75,rely = 0.5,anchor = tk.CENTER)

is_repeat = tk.BooleanVar()
repeat_check = tk.Checkbutton(root,text = 'Repeat',variable = is_repeat)
repeat_check.place(relx = 0.55,rely = 0.5,anchor = tk.CENTER)

is_autoplay = tk.BooleanVar()
autoplay_check = tk.Checkbutton(root,text = 'Autoplay',variable = is_autoplay)
autoplay_check .place(relx = 0.825,rely = 0.5,anchor = tk.CENTER)

#Checks every 5 seconds if the song is over, and acts according to is_repeat
def check_if_over():
    if queue.head != None:
        if queue.head.song.timer.curr_time > queue.head.song.total_time:
            if is_repeat.get():
                queue.head.song.play()
            else:
                #check if autoplay is on
                if is_autoplay.get():
                    next_in_queue()
                    queue.head.song.play()
                    
    root.after(5000,check_if_over)
check_if_over()
'''End of Queue Frame and Canvas'''


'''Beginning of Query and Selection'''
#Outer selection frame, contains both the scrollbar and the canvas
selection_frame_out = tk.Frame(root,width = 300,height = 600,bg = 'white',
                           highlightbackground = 'black',highlightthickness = 1)
selection_frame_out.place(relx = 0.2,rely = 0.5,anchor = tk.CENTER)

selection_canvas = tk.Canvas(selection_frame_out,width = 300,height = 600,
                             bg = 'white')
selection_canvas.pack(side = tk.LEFT,fill = tk.BOTH,expand = 0)

selection_scroll = ttk.Scrollbar(selection_frame_out,orient = tk.VERTICAL,
                                command = selection_canvas.yview)
selection_scroll.pack(side = tk.RIGHT,fill = tk.Y)

selection_canvas.configure(yscrollcommand = selection_scroll.set)
selection_canvas.bind("<Configure>",lambda e: selection_canvas.config(scrollregion = selection_canvas.bbox(tk.ALL)))

#Contains only the scrollable content
selection_frame_in = tk.Frame(selection_canvas,width = 300,height = 600,
                              bg = 'white')
selection_canvas.create_window((0,0),window = selection_frame_in,anchor = tk.NW)

song_widgets = []

#Frame for displaying music canvas
music_frame = tk.Frame(root,width = 600,height = 250,bg = 'light gray')
music_frame.place(relx = 0.65,rely = 0.7,anchor = tk.CENTER)
tk.Label(music_frame,text = 'Music Goes Here',
         bg = 'light gray').place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)



#Takes an array of Music Items as input and fills the selection canvas
#with relevant data
def fill_selection(songs):
    #Tool to load new Song and get rid of old one
    def load_new_song(song):
        if last_song_window != [None]:
            last_song_window[0].destroy()
        last_song_window[0] = song.to_canvas(music_frame)
        last_song_window[0].place(relx = 0.5, rely = 0.5,anchor = tk.CENTER)
        song.load()
        queue.replace_head(Node(song))
        fill_queue()

    def add_song_to_queue(song):
        queue.add_node(Node(song))
        fill_queue()
        
        
    #Get rid of all former widgets
    for j in range(len(song_widgets)):
        song_widgets[j].destroy()
        
    song_widgets.clear()
    i = 0
    last_category = ''
    for song in songs:
        if song.category != last_category:
            last_category = song.category
            song_widgets.append(tk.Label(selection_frame_in,text = song.category + ':'))
            song_widgets[i].grid(row = i,sticky = tk.W)
            i+=1
            
            
        song_widgets.append(tk.Label(selection_frame_in,text = '   '+song.name,font = ('Ariel',12)))
        song_widgets[i].grid(row = i,column = 0,pady = 5,sticky = tk.W)
        i+=1
        
        song_widgets.append(tk.Button(selection_frame_in,text = 'I>',width = 4,height = 2,
                                      command = lambda song = song: load_new_song(song)))
        song_widgets[i].grid(row = i-1,column = 1,padx = 10)
        i+=1

        song_widgets.append(tk.Button(selection_frame_in,text = 'Q',width = 4,height = 2,
                                      command = lambda song = song: add_song_to_queue(song)))
        song_widgets[i].grid(row = i-2,column = 2,padx = 2)
        i+=1

    corrector = tk.Label(selection_frame_in,text = '',bg = 'white')
    song_widgets.append(corrector)
    corrector.grid(row = i-2,column = 0,pady = 20)

    selection_canvas.configure(scrollregion = selection_canvas.bbox(tk.ALL))


fill_selection(music_array.array)



def open_query():
    query_level = tk.Toplevel(root)
    query_level.title('Query')
    query_level.geometry('300x300+200+200')
    tk.Label(query_level,text = 'Search').place(relx = 0.5,
                                                rely = 0.05,anchor = tk.CENTER)
    
    tk.Label(query_level,text = 'Name').place(relx = 0.25,
                                              rely = 0.1,anchor = tk.CENTER)
    name_entry = tk.Entry(query_level)
    name_entry.place(relx = 0.25,rely = 0.175,anchor = tk.CENTER)

    tk.Label(query_level,text = 'Category').place(relx = 0.75,
                                                  rely = 0.1,anchor = tk.CENTER)
    category_entry = tk.Entry(query_level)
    category_entry.place(relx = 0.75,rely = 0.175,anchor = tk.CENTER)

    tk.Label(query_level,text = 'Options').place(relx = 0.5,rely = 0.3,
                                                      anchor = tk.CENTER)

    #Radiobuttons to decide which gate to use

    def query_music():
        name = name_entry.get()
        category = category_entry.get()
        results = music_array.query_to_list(name,category,
                                            gate = select_gate.get())
        fill_selection(results)


        
    tk.Label(query_level,text = 'Search Gate').place(relx = 0.25,rely = 0.4,
                                                     anchor = tk.CENTER)
    select_gate = tk.StringVar(query_level,value = 'and')
    and_radio = tk.Radiobutton(query_level,text = 'and',variable = select_gate,
                               value = 'and')
    and_radio.place(relx = 0.15,rely = 0.475,anchor = tk.W)
    or_radio = tk.Radiobutton(query_level,text = 'or',variable = select_gate,
                               value = 'or')
    or_radio.place(relx = 0.15,rely = 0.55,anchor = tk.W)
    not_radio = tk.Radiobutton(query_level,text = 'not',variable = select_gate,
                               value = 'not')
    not_radio.place(relx = 0.15,rely = 0.625,anchor = tk.W)

    
    search_button = tk.Button(query_level,text = 'Search!',width = 10,
                              command = query_music)
    search_button.place(relx = 0.25,rely = 0.925,anchor = tk.CENTER)

    close_button = tk.Button(query_level,text = 'Close',width = 10,
                              command = query_level.destroy)
    close_button.place(relx = 0.75,rely = 0.925,anchor = tk.CENTER)

    query_level.mainloop()


    

query_button = tk.Button(root,text = 'Query',width = 10,height = 2,
                         command = open_query)
query_button.place(relx = 0.2,rely = 0.08,anchor = tk.CENTER)

'''End of Query and Selection'''





'''Beginning of Adding a new Song'''
def add_new_song():
    song_level = tk.Toplevel(root)
    song_level.title('Add New Song')
    song_level.geometry('750x250+200+600')

    tk.Label(song_level,text = '* = Required',font = ('Ariel',8)).place(relx = 0.925,rely = 0.06,anchor = tk.CENTER)

    #Name
    tk.Label(song_level,text = 'Name *').place(relx = 0.2,rely = 0.075,anchor = tk.CENTER)
    name_entry = tk.Entry(song_level)
    name_entry.place(relx = 0.2,rely = 0.175,anchor = tk.CENTER)

    #Path
    tk.Label(song_level,text = 'Path *').place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)
    path_entry = tk.Entry(song_level,width = 40)
    path_entry.insert(0,'mp3_files/*put your song here*.mp3')
    path_entry.place(relx = 0.5,rely = 0.175,anchor = tk.CENTER)

    #Author
    tk.Label(song_level,text = 'Author').place(relx = 0.8,rely = 0.075,anchor = tk.CENTER)
    author_entry = tk.Entry(song_level)
    author_entry.place(relx = 0.8,rely = 0.175,anchor = tk.CENTER)

    #Intervals
    tk.Label(song_level,text = 'Intervals').place(relx = 0.5,rely = 0.325,anchor = tk.CENTER)
    interval_entry = tk.Entry(song_level,width = 30)
    interval_entry.insert(0,'0.0,')
    interval_entry.place(relx = 0.5,rely = 0.425,anchor = tk.CENTER)

    #Total Time
    tk.Label(song_level,text = 'Length(Seconds) *').place(relx = 0.8,rely = 0.325,anchor = tk.CENTER)
    total_entry = tk.Entry(song_level)
    total_entry.insert(0,'60.0')
    total_entry.place(relx = 0.8,rely = 0.425,anchor = tk.CENTER)

    #Category
    tk.Label(song_level,text = 'Category').place(relx = 0.5,rely = 0.575,anchor = tk.CENTER)
    category_entry = tk.Entry(song_level)
    category_entry.place(relx = 0.5,rely = 0.675,anchor = tk.CENTER)


    def test_song():
        test_level = tk.Toplevel(song_level)

        file_path = Path(path_entry.get())
        if file_path.is_file():
            #Datavengers, Assemble
            name = name_entry.get()
            path = path_entry.get()
            author = author_entry.get()
            intervals = []
            #Gather intervals and split into floats
            for interval in interval_entry.get().split(','):
                if interval.replace('.','').isdecimal():
                    intervals.append(float(interval))
            
            total_time = float(total_entry.get())
            category = category_entry.get()

            
            test_song = Music(name,path,author = author,intervals = intervals,
                              total_time = total_time,category = category)
            test_song.to_canvas(test_level).pack()
            
        else:
            tk.Label(test_level,text = 'Error, Path not found').pack()

        tk.Button(test_level,text = 'Close',width = 10,command = test_level.destroy).pack()

    test_button = tk.Button(song_level,text = 'Test Song',width = 10,command = test_song)
    test_button.place(relx = 0.9,rely = 0.85,anchor = tk.CENTER)

    def add_song():

        name = name_entry.get()
        path = path_entry.get()
        file_path = Path(path)

        intervals = []
        #Gather intervals and split into floats
        for interval in interval_entry.get().split(','):
            if interval.replace('.','').replace(' ','').isdecimal():
                intervals.append(float(interval))
                
        #If path isn't a file, do nothing
        if not file_path.is_file():
            error_level = tk.Toplevel(song_level)
            tk.Label(error_level,text = 'Error, Path not found').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        #If the name is blank, do nothing
        elif name == '':
            error_level = tk.Toplevel(song_level)
            tk.Label(error_level,text = 'Error, invalid Name').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        
        author = author_entry.get()    
        total_time = float(total_entry.get())
        category = category_entry.get()

        new_song = Music(name,path,author = author,intervals = intervals,
                         total_time = total_time,category = category)
        music_array.add_ordered(new_song)
        fill_selection(music_array.array)
        song_level.destroy()
        
        

    done_button = tk.Button(song_level,text = 'Done',width = 10,command = add_song)
    done_button.place(relx = 0.425,rely = 0.9,anchor = tk.CENTER)

    cancel_button = tk.Button(song_level,text = 'Cancel',width = 10,command = song_level.destroy)
    cancel_button.place(relx = 0.575,rely = 0.9,anchor = tk.CENTER)
    

    
    
newsong_button = tk.Button(root,text = 'Add Song',width = 10,command = add_new_song)
newsong_button.place(relx = 0.2,rely = 0.9075,anchor = tk.CENTER)
'''End of Adding a new Song'''

'''Beginning of editing songs'''

#Works by taking a song, copying its elements, and replacing the old one with the new one
def open_editing(song):
    editing_level = tk.Toplevel(root)
    editing_level.title(f'Editing {song.name}')
    editing_level.geometry('750x250+200+600')

    #Song to replace old one
    song2 = Music('New','Song')

    #Name
    tk.Label(editing_level,text = 'Name *').place(relx = 0.2,rely = 0.075,anchor = tk.CENTER)
    name_entry = tk.Entry(editing_level)
    name_entry.insert(0,song.name)
    name_entry.place(relx = 0.2,rely = 0.175,anchor = tk.CENTER)

    #Path
    tk.Label(editing_level,text = 'Path *').place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)
    path_entry = tk.Entry(editing_level,width = 40)
    path_entry.insert(0,song.path)
    path_entry.place(relx = 0.5,rely = 0.175,anchor = tk.CENTER)

    #Author
    tk.Label(editing_level,text = 'Author').place(relx = 0.8,rely = 0.075,anchor = tk.CENTER)
    author_entry = tk.Entry(editing_level)
    author_entry.insert(0,song.author)
    author_entry.place(relx = 0.8,rely = 0.175,anchor = tk.CENTER)

    #Intervals
    tk.Label(editing_level,text = 'Intervals').place(relx = 0.5,rely = 0.325,anchor = tk.CENTER)
    interval_entry = tk.Entry(editing_level,width = 30)
    interval_entry.insert(0,str(song.intervals).replace('[','').replace(']',''))
    interval_entry.place(relx = 0.5,rely = 0.425,anchor = tk.CENTER)

    #Total Time
    tk.Label(editing_level,text = 'Length(Seconds) *').place(relx = 0.8,rely = 0.325,anchor = tk.CENTER)
    total_entry = tk.Entry(editing_level)
    total_entry.insert(0,song.total_time)
    total_entry.place(relx = 0.8,rely = 0.425,anchor = tk.CENTER)

    #Category
    tk.Label(editing_level,text = 'Category').place(relx = 0.5,rely = 0.575,anchor = tk.CENTER)
    category_entry = tk.Entry(editing_level)
    category_entry.insert(0,song.category)
    category_entry.place(relx = 0.5,rely = 0.675,anchor = tk.CENTER)

    def write_edits():
        name = name_entry.get()
        path = path_entry.get()
        file_path = Path(path)
                
        #If path isn't a file, do nothing
        if not file_path.is_file():
            error_level = tk.Toplevel(song_level)
            tk.Label(error_level,text = 'Error, Path not found').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        
        intervals = []

        #Gather intervals and split into floats
        for interval in interval_entry.get().split(','):
            if interval.replace('.','').replace(' ','').isdecimal():
                intervals.append(float(interval))

        song2.name = name
        song2.path = path
        song2.author = author_entry.get()
        song2.intervals = intervals
        song2.total_time = float(total_entry.get())
        song2.category = category_entry.get()

        music_array.remove(song)
        music_array.add_ordered(song2)
        
        fill_selection(music_array.array)
        
        editing_level.destroy()
        

    done_button = tk.Button(editing_level,text = 'Done',width = 10,command = write_edits)
    done_button.place(relx = 0.4,rely = 0.9,anchor = tk.CENTER)

    cancel_button = tk.Button(editing_level,text = 'Cancel',width = 10,command = editing_level.destroy)
    cancel_button.place(relx = 0.6,rely = 0.9,anchor = tk.CENTER)

    
#Actual method the user calls upon by calling the Edit Song button
#Will call open_editing after a song is selected
def open_editing_choices():
    choice_level = tk.Toplevel(root)
    choice_level.title('Choose a Song')
    choice_level.geometry('300x450+200+200')

    tk.Label(choice_level,text = 'Choose a Song to Edit').place(relx = 0.5,rely = 0.05,anchor = tk.CENTER)

    #Scrollbar Tomfoolery
    edit_frame_out = tk.Frame(choice_level,width = 50,height = 70,bg = 'white',
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
    edit_canvas.create_window((0,0),window = edit_frame_in,anchor = tk.NW)

    des_song = tk.IntVar(edit_frame_in)

    for i in range(music_array.length()):
        rb = tk.Radiobutton(edit_frame_in,text = music_array.get(i).name,
                            variable = des_song,value = i)
        rb.grid(row = i,column = 0,pady = 2,sticky = tk.W)

        #Wow if only lambda could have more than 1 void function call
        def bridge_editing():
            open_editing(music_array.get(des_song.get()))
            choice_level.destroy()
        
    select_button = tk.Button(choice_level,text = 'Select',width = 10,
                              command = bridge_editing)
    select_button.place(relx = 0.5,rely = 0.8,anchor = tk.CENTER)

    cancel_button = tk.Button(choice_level,text = 'Cancel',width = 10,command = choice_level.destroy)
    cancel_button.place(relx = 0.5,rely = 0.9,anchor = tk.CENTER)

editsong_button = tk.Button(root,text = 'Edit Song',width = 10,command = open_editing_choices)
editsong_button.place(relx = 0.125,rely = 0.9075,anchor = tk.CENTER)

'''End of editing songs'''

'''Beginning of Deleting Songs'''
def open_delete():
    del_level = tk.Toplevel(root)
    del_level.title('Delete Songs')
    del_level.geometry('300x600+200+200')

    tk.Label(del_level,text = 'Select Songs to Delete').place(relx = 0.5,rely = 0.05,anchor = tk.CENTER)

    #Scrollbar Tomfoolery
    del_frame_out = tk.Frame(del_level,width = 50,height = 100,bg = 'white',
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
    boolvars = []
    for i in range(music_array.length()):
        boolvars.append(tk.BooleanVar(del_frame_in))
    
    for i in range(len(boolvars)):
        cb = tk.Checkbutton(del_frame_in,text = music_array.get(i).name,variable = boolvars[i],
                            onvalue = True,offvalue = False)
        cb.grid(row = i,column = 0,pady = 2,sticky = tk.W)

    

    #Sets each booleanvar in boolvars to not itself
    def toggle_all():
        for i in range(len(boolvars)):
            boolvars[i].set(not boolvars[i].get())

    def delete_songs():
        #Make a list of all songs to be deleted
        to_delete = []
        for i in range(len(boolvars)):
            if boolvars[i].get():
                to_delete.append(music_array.get(i))
        #Iterate through list and delete each one
        for song in to_delete:
            music_array.remove(song)

        fill_selection(music_array.array)
            
        del_level.destroy()
        
    
    toggle_button = tk.Button(del_level,text = 'Toggle All',width = 8,height = 2,command = toggle_all)
    toggle_button.place(relx = 0.5,rely = 0.825,anchor = tk.CENTER)

    done_button = tk.Button(del_level,text = 'Delete',width = 10,command = delete_songs)
    done_button.place(relx = 0.8,rely = 0.9,anchor = tk.CENTER)

    cancel_button = tk.Button(del_level,text = 'Cancel',width = 10,command = del_level.destroy)
    cancel_button.place(relx = 0.8,rely = 0.95,anchor = tk.CENTER)



        
        
deletesong_button = tk.Button(root,text = 'Delete Songs',width = 10,command = open_delete)
deletesong_button.place(relx = 0.275,rely = 0.9075,anchor = tk.CENTER)
'''End of Deleting Songs'''

#The data will be kept in an array for ease of access
save_button = tk.Button(root,text = 'Save',width = 10,command = lambda: saving.save_df(music_array.to_df()))
save_button.place(relx = 0.2,rely = 0.95,anchor = tk.CENTER)


quit_button = tk.Button(root,text = 'Quit',width = 10,height = 2,command = quit_minstrel)
quit_button.place(relx = 0.9,rely = 0.925,anchor = tk.CENTER)


root.mainloop()

