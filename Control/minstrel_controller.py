import tkinter as tk
from sys import path

path.insert(0,'../Model')
path.insert(0,'../View')

from minstrel_view import *
from minstrel_data import *
from music_data import Music,kill_mixer
from music_controller import MusicController

def make_controller(root):
    mc = MinstrelController(is_frame = True,root = self.hv.root)
    return mc

def bind_button(button,command):
    button.configure(command = command)

class MinstrelController:

    def __init__(self,**kwargs):
        self.fw = FileWriter()
        self.music_array = self.fw.save_to_music_array()
        self.queue = LinkedList()
        self.main = None

        root = kwargs.get('root',None)
        if root != None:
            self.main = MinstrelView(is_frame = True,root = root,
                                     music_array = self.music_array,queue = self.queue)
        else:
            self.main = MinstrelView(music_array = self.music_array,queue = self.queue)

        #Keeps track of how many songs are in the selection frame
        self.present_songs = self.music_array.array
        self.fill_selection()
        self.fill_queue()

        
        bind_button(self.main.shuffle_button,self.shuffle)
        
        bind_button(self.main.next_button,self.next_in_queue)
        bind_button(self.main.clear_button,lambda: self.fill_queue(clear = True))
        
        bind_button(self.main.query_button,self.make_query_level)
        bind_button(self.main.undo_query_button,self.undo_query)

        bind_button(self.main.newsong_button,self.make_new_song_level)
        bind_button(self.main.editsong_button,self.make_select_song_level)
        bind_button(self.main.deletesong_button,self.make_delete_song_level)

        
        bind_button(self.main.save_button,self.save_music)
        bind_button(self.main.quit_button,self.quit_minstrel)


        
        
        self.main.root.protocol('WM_DELETE_WINDOW',self.quit_minstrel)
        
        self.check_if_over()
        self.main.root.mainloop()

        
        
    #Selection Frame Methods

    def load_new_song(self,song):
        if self.main.last_song_window != None:
            self.main.last_song_window.destroy()
        controller = MusicController(song)
        self.main.last_song_window = controller.create_canvas(self.main.music_frame).music_canvas
        song.load()
        self.queue.replace_head(Node(song))
        self.fill_queue()
        
    def add_song_to_queue(self,song,**kwargs):
        self.queue.add_node(Node(song))
        adjust_frame = kwargs.get('adjust_frame',True)
        if adjust_frame:
            self.fill_queue()

    
    def load_by_category(self,cat):
        for song in self.present_songs:
            if song.category == cat:
                self.add_song_to_queue(song,adjust_frame = False)
        self.fill_queue()

    def queue_everything(self):
        for song in self.present_songs:
            self.add_song_to_queue(song,adjust_frame = False)
        self.fill_queue()

    def on_frame_configure(self,event):
        self.main.selection_canvas.configure(scrollregion = self.main.selection_canvas.bbox(tk.ALL))

    def fill_selection(self):
        #Get rid of all former widgets
        for i in range(len(self.main.song_widgets)):
            for j in range(len(self.main.song_widgets[i])):
                self.main.song_widgets[i][j].destroy()
                
        self.main.song_widgets.clear()
        #Note: i represents the row in which each widget resides
        self.main.song_widgets.append([tk.Button(self.main.selection_frame_in,text = 'Q All',
                                   width = 10,height = 2,command = self.queue_everything)])
        self.main.song_widgets[0][0].grid(row = 0,column = 0,pady = 20)
        i = 1
        j = 0
        last_category = ''
        for song in self.present_songs:
            if song.category != last_category:
                self.main.song_widgets.append([])
                last_category = song.category
                self.main.song_widgets[i].append(tk.Label(self.main.selection_frame_in,text = song.category + ':'))
                self.main.song_widgets[i][0].grid(row = i,sticky = tk.W)
                self.main.song_widgets[i].append(tk.Button(self.main.selection_frame_in,text = 'Q Cat',width = 8,
                                                 command = lambda cat = song.category: self.load_by_category(cat)))
            
                self.main.song_widgets[i][1].grid(row = i,column = 2,pady = 10)
                i+=1
                
            self.main.song_widgets.append([])
            self.main.song_widgets[i].append(tk.Label(self.main.selection_frame_in,text = '   '+song.name,font = ('Ariel',12)))
            self.main.song_widgets[i][0].grid(row = i,column = 0,pady = 5,sticky = tk.W)
            
            self.main.song_widgets[i].append(tk.Button(self.main.selection_frame_in,text = 'I>',width = 4,height = 2,
                                          command = lambda song = song: self.load_new_song(song)))
            self.main.song_widgets[i][1].grid(row = i,column = 1,padx = 10)

            self.main.song_widgets[i].append(tk.Button(self.main.selection_frame_in,text = 'Q',width = 4,height = 2,
                                          command = lambda song = song: self.add_song_to_queue(song)))
            self.main.song_widgets[i][2].grid(row = i,column = 2,padx = 2)
            i+=1

        corrector = tk.Label(self.main.selection_frame_in,text = '\n\n\n\n',bg = 'white')
        self.main.song_widgets.append([corrector])
        corrector.grid(row = i,column = 0,pady = 20)

        self.main.selection_frame_in.bind('<Configure>',self.on_frame_configure)
        self.main.selection_canvas.yview_moveto(0.0)

    #Queue Frame Methods

    #Skips to node of param skips
    def go_to_node(self,skips):
        n = self.queue.head
        for i in range(skips):
            n = n.next
        self.queue.head = n
        if self.main.last_song_window != None:
            self.main.last_song_window.destroy()
        controller = MusicController(self.queue.head.song)
        self.main.last_song_window = controller.create_canvas(self.main.music_frame).music_canvas
        self.main.last_song_window.place(relx = 0.5, rely = 0.5,anchor = tk.CENTER)
        self.queue.head.song.load()
        self.fill_queue()
        self.main.queue_canvas.configure(scrollregion = self.main.queue_canvas.bbox(tk.ALL))

    #Removes a Node from the Queue and updates the GUI
    def remove_node(self,song):
        self.queue.remove_music(song)
        self.fill_queue()
        self.main.queue_canvas.configure(scrollregion = queue_canvas.bbox(tk.ALL))
    
    def remove_node_index(self,index):
        self.queue.remove_index(index)
        self.fill_queue()
        self.main.queue_canvas.configure(scrollregion = self.main.queue_canvas.bbox(tk.ALL))

    def on_queue_frame_configure(self,event):
        self.main.queue_canvas.configure(scrollregion = self.main.queue_canvas.bbox(tk.ALL))
        
    def fill_queue(self,**kwargs):
        #Resets the queue to a blank linked list
        is_clear = kwargs.get('clear',False)
        if bool(is_clear):
            self.queue.head = None
            
        #Clear the Queue frame to make way for new widgets
        for i in range(len(self.main.queue_widgets)):
            self.main.queue_widgets[i].destroy()

        self.main.queue_widgets.clear()
        
        #If the queue is empty, do nothing
        if self.queue.head == None:
            self.main.queue_widgets.append(tk.Label(self.main.queue_canvas,text = 'Queue Empty'))
            self.main.queue_widgets[0].place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)
            return
        #Note: There is a problem with the scrollbar not adjusting correctly for the first iteration
        #Considering that the user will not need to scroll until a couple of songs have been added to the queue
        #This issue doesn't mean much (Knock on wood)

        n = self.queue.head
        i = 0
        song_index = 0
        while n != None:
            self.main.queue_widgets.append(tk.Button(self.main.queue_frame_in,text = n.song.name,command = lambda i=song_index:self.go_to_node(i)))
            self.main.queue_widgets[i].grid(row = 0,column = i//2,padx = 10,pady = 30)
            i+=1
            self.main.queue_widgets.append(tk.Button(self.main.queue_frame_in,text = 'Remove',width = 8,command = lambda index=song_index:self.remove_node_index(index)))
            self.main.queue_widgets[i].grid(row = 1,column = i//2,padx = 10)
            i+=1
            song_index+=1
            
            n = n.next
            
        #To fix the scrollbar not reaching all the widgets        (Wow that's a lot of spaces)
        corrector = tk.Label(self.main.queue_frame_in,text = '                                                          ',bg = 'white')
        self.main.queue_widgets.append(corrector)
        corrector.grid(row = 0,column = i+1,padx = 10)

        self.main.queue_frame_in.bind('<Configure>',self.on_queue_frame_configure)
        self.main.queue_canvas.xview_moveto(0.0)
        

    def next_in_queue(self):
        #If either head or head.next is null, do nothing
        if self.queue.head == None or self.queue.head.next == None:
            return
        self.queue.head = self.queue.head.next

        if self.main.last_song_window != None:
            self.main.last_song_window.destroy()
        controller = MusicController(self.queue.head.song)
        self.main.last_song_window = controller.create_canvas(self.main.music_frame).music_canvas
        self.main.last_song_window.place(relx = 0.5, rely = 0.5,anchor = tk.CENTER)
        self.queue.head.song.load()
        self.fill_queue()

    def shuffle(self):
        temp = self.queue.randomize()
        #For some reason, reassigning the queue pointer doesn't work, so I gotta do this the hard way
        self.queue.head = temp.head
        if self.queue.head != None:
            self.load_new_song(self.queue.head.song)
        self.fill_queue()

    def check_if_over(self):
        if self.queue.head != None:
            if self.queue.head.song.timer.curr_time > self.queue.head.song.total_time:
                if self.main.is_repeat.get():
                    self.queue.head.song.play()
                #check if autoplay is on
                elif self.main.is_autoplay.get():
                    self.next_in_queue()
                    self.queue.head.song.play()
                    
        self.main.root.after(5000,self.check_if_over)
    
    
    #Query Methods
    def make_query_level(self):
        #Singleton
        if self.main.query_level != None and self.main.query_level.query_level.winfo_exists():
            self.main.query_level.query_level.lift()
            return
        
        ql = QueryLevel(self.main.root)
        self.main.query_level = ql

        bind_button(ql.search_button,self.query_music)
        
        ql.query_level.mainloop()
        
        

    def query_music(self):
        ql = self.main.query_level
        name = ql.name_entry.get()
        category = ql.category_entry.get()
        self.present_songs = self.music_array.query_to_list(name,category,
                                            gate = ql.select_gate.get())
        self.fill_selection()

    def undo_query(self):
        self.present_songs = self.music_array.query_to_list('','')
        self.fill_selection()
        self.main.selection_canvas.configure(scrollregion = self.main.selection_canvas.bbox(tk.ALL))

    #Testing Song Method
    def make_test_song_level(self,root,song):
        test_level = tk.Toplevel(root)
        controller = MusicController(song)
        controller.create_canvas(test_level).music_canvas.pack()
        tk.Button(test_level,text = 'Close Test',
                  command = test_level.destroy).pack()
        

    #Adding Song Methods

    def test_from_new_song(self):
        from pathlib import Path
        
        nsl = self.main.new_song_level
        path = nsl.path_entry.get()

        file_path = Path(f'../Saving/{path}')
        if file_path.is_file():
            #Datavengers, Assemble
            name = nsl.name_entry.get()
            path = nsl.path_entry.get()
            author = nsl.author_entry.get()
            intervals = []
            #Gather intervals and split into floats
            for interval in nsl.interval_entry.get().split(','):
                if interval.replace('.','').isdecimal():
                    intervals.append(float(interval))
            
            total_time = float(nsl.total_entry.get())
            category = nsl.category_entry.get()

            
            test_song = Music(name,path,author = author,intervals = intervals,
                              total_time = total_time,category = category)
            self.make_test_song_level(nsl.song_level,test_song)
            
        else:
            error_level = tk.Toplevel(nsl.song_level)
            tk.Label(error_level,text = 'Error, path not found').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            
        

    def make_new_song_level(self):
        #Singleton
        if self.main.new_song_level != None and self.main.new_song_level.song_level.winfo_exists():
            self.main.new_song_level.song_level.lift()
            return
        
        nsl = NewSongLevel(self.main.root)
        self.main.new_song_level = nsl
        bind_button(nsl.done_button,self.add_song)
        bind_button(nsl.test_button,self.test_from_new_song)


    def add_song(self):
        from pathlib import Path
        
        nsl = self.main.new_song_level
        
        name = nsl.name_entry.get()
        path = nsl.path_entry.get()
        file_path = Path(f'../Saving/{path}')

        intervals = []
        #Gather intervals and split into floats
        for interval in nsl.interval_entry.get().split(','):
            if interval.replace('.','').replace(' ','').isdecimal():
                intervals.append(float(interval))
        #If is_ten, insert intervals from 0 to song length by 10
        if nsl.is_ten.get():
            for i in range(20,math.trunc(float(total_entry.get())),20):
                intervals.append(float(i))
            intervals.sort()
                
        #If path isn't a file, do nothing
        if not file_path.is_file():
            error_level = tk.Toplevel(nsl.song_level)
            tk.Label(error_level,text = 'Error, Path not found').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        #If the name is blank, do nothing
        elif name == '':
            error_level = tk.Toplevel(nsl.song_level)
            tk.Label(error_level,text = 'Error, invalid Name').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        elif len(name) > 24:
            error_level = tk.Toplevel(nsl.song_level)
            tk.Label(error_level,text = 'Error, name > 24 chars').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        
        author = nsl.author_entry.get()    
        total_time = float(nsl.total_entry.get())
        category = nsl.category_entry.get()

        new_song = Music(name,path,author = author,intervals = intervals,
                         total_time = total_time,category = category)
        #print(new_song)
        self.music_array.add_ordered(new_song)
        
        nsl.song_level.destroy()
        
        self.fill_selection()
        
    
    #Editing Song Methods
    def make_select_song_level(self):
        #Singleton
        if self.main.select_song_level != None and self.main.select_song_level.choice_level.winfo_exists():
            self.main.select_song_level.choice_level.lift()
            return
        if self.main.edit_song_level != None and self.main.edit_song_level.editing_level.winfo_exists():
            return
        
        ssl = SelectSongLevel(self.main.root,self.music_array.array)
        self.main.select_song_level = ssl

        bind_button(ssl.select_button,lambda: self.make_edit_song_level(ssl.des_song.get()))
                
    def make_edit_song_level(self,index):
        self.main.select_song_level.choice_level.destroy()
        esl = EditSongLevel(self.main.root,self.music_array.array[index])
        self.main.edit_song_level = esl

        bind_button(esl.done_button,lambda: self.write_edits(self.music_array.array[index]))
                
    def write_edits(self,old_song):
        from pathlib import Path
        
        esl = self.main.edit_song_level
        new_song = Music('New','Song')

        name = esl.name_entry.get()
        path = esl.path_entry.get()
        file_path = Path(f'../Saving/{path}')
        
        #If path isn't a file, do nothing
        if not file_path.is_file():
            error_level = tk.Toplevel(esl.editing_level)
            tk.Label(error_level,text = 'Error, Path not found').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        elif name == '':
            error_level = tk.Toplevel(esl.editing_level)
            tk.Label(error_level,text = 'Error, invalid Name').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        elif len(name) > 24:
            error_level = tk.Toplevel(esl.editing_level)
            tk.Label(error_level,text = 'Error, name > 24 chars').pack()
            tk.Button(error_level,text = 'Close',command = error_level.destroy).pack()
            return
        
        intervals = []

        #Gather intervals and split into floats
        for interval in esl.interval_entry.get().split(','):
            if interval.replace('.','').replace(' ','').isdecimal():
                intervals.append(float(interval))
        #If is_ten, insert intervals from 0 to song length by 10
        if esl.is_ten.get():
            for i in range(20,math.trunc(float(esl.total_entry.get())),20):
                intervals.append(float(i))
            intervals.sort()

        new_song.name = name
        new_song.path = path
        new_song.author = esl.author_entry.get()
        new_song.intervals = intervals
        new_song.total_time = float(esl.total_entry.get())
        new_song.category = esl.category_entry.get()

        self.music_array.remove(old_song)
        self.music_array.add_ordered(new_song)
        self.fill_selection()

        esl.editing_level.destroy()

    #Deleting Song Methods
    def make_delete_song_level(self):
        #Singleton
        if self.main.delete_song_level != None and self.main.delete_song_level.del_level.winfo_exists():
            self.main.delete_song_level.del_level.lift()
            return
        
        dsl = DeleteSongLevel(self.main.root,self.music_array.array)
        self.main.delete_song_level = dsl
        bind_button(dsl.done_button,self.delete_songs)
        bind_button(dsl.toggle_button,self.toggle_boolvars)

        

        dsl.del_level.mainloop()


    def delete_songs(self):
        dsl = self.main.delete_song_level

        to_delete = []
        
        for i in range(len(dsl.boolvars)):
            if dsl.boolvars[i].get():
                to_delete.append(self.music_array.get(i))

        for song in to_delete:
            self.music_array.remove(song)

        self.fill_selection()

        dsl.del_level.destroy()

    def toggle_boolvars(self):
        dsl = self.main.delete_song_level
        for i in range(len(dsl.boolvars)):
            dsl.boolvars[i].set(not dsl.boolvars[i].get())

    #Saving and Quitting Methods

    def save_music(self):
        self.fw.save_df(self.music_array.to_df())
        

    def quit_minstrel(self):
        kill_mixer()
        self.main.root.destroy()
    


if __name__ == '__main__':
        
    mc = MinstrelController()

    

