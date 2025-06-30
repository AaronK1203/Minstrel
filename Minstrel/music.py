import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import tkinter as tk
from minstrel_clock import Clock
from pygame import mixer


mixer.init()

def kill_mixer():
        mixer.quit()
        #print('Killed Mixer')

class Music:

    #Records what music is being played at a given time with a name
    active_mp3 = None
    
    
    def __init__(self,name,path,**kwargs):
        self.name = name
        self.path = path
        self.author = kwargs.get('author','unknown')
        self.intervals = kwargs.get('intervals',[0.0])
        self.bpm = kwargs.get('bpm',60)
        self.category = kwargs.get('category','')
        self.total_time = kwargs.get('total_time',6000)
        
        self.timer = Clock(0)
        

    def __str__(self):
        return f'{self.name},{self.path},{self.intervals},{self.bpm},{self.total_time},{self.category}'
        
    def compare_to(self,other):
        #Compare categories by alphabetical order
        if self.category > other.category:
            return 1
        elif self.category < other.category:
            return -1
        else:
            #Compare names
            if self.name > other.name:
                return 1
            elif self.name < other.name:
                return -1
            else:
                return 0
        
    def set_name(self,name):
        self.name = name

    def set_path(self,path):
        self.path = path
        
    #Intervals are timestamps of important parts of each song
    def set_intervals(self,intervals):
        self.intervals = intervals

    def load(self):
        mixer.music.load(self.path)
        self.active_mp3 = self.name

    def play(self):
        mixer.music.load(self.path)
        mixer.music.play()
        self.timer.curr_time = 0
        self.timer.increment_value = 0.5

    def play_from(self,timestamp):
        mixer.set_pos(timestamp)
        self.timer.curr_time = timestamp

    def pause(self):
        mixer.music.pause()
        self.timer.increment_value = 0

    def unpause(self):
        mixer.music.unpause()
        self.timer.increment_value = 0.5

    def stop(self):
        mixer.music.stop()
        self.timer.increment_value = 0
    

    def to_window(self,root):
        music_level = tk.Toplevel(root)
        music_level.title(self.name)
        music_level.geometry('600x300+500+500')

        music_canvas = tk.Canvas(music_level,width = 500,height = 150,bg = 'white')
        music_canvas.place(relx = 0.5,rely = 0.4,anchor = tk.CENTER)

        music_canvas.create_rectangle(2,2,500,150,outline = 'black')
        music_canvas.create_line(50,75,450,75)

        progress_line = music_canvas.create_line(50,70,50,80)

        #Records the x-position for the Progress Bar
        x_loc = 50.0
        latest_timestamp = 0.0

        '''Beginning of Progress line graphics'''
        def update_progress():
            nonlocal x_loc
            nonlocal latest_timestamp
            nonlocal progress_line
            #If the current song playing isn't the one whose progress is being checked, do nothing
            if self.active_mp3 != self.name:
                pass
            #If mixer isn't on, do nothing
            elif not mixer.music.get_busy():
                pass
            #If song is done, do nothing
            elif x_loc > self.total_time:
                pass
            else:
                music_canvas.delete(progress_line)
                x_loc = latest_timestamp + ((mixer.music.get_pos()/1000)/self.total_time)*400
                
                progress_line = progress_line = music_canvas.create_line(x_loc,70,x_loc,80)
            music_level.after(1000,update_progress)

        update_progress()

                

        '''End of Progress Line Graphics'''

        '''Beginning of Interval buttons'''


        def play_from(timestamp):
            nonlocal x_loc
            nonlocal latest_timestamp
            #If the current song playing isn't the one whose button was clicked, do nothing
            if self.active_mp3 != self.name:
                print('error')
                return
            if not mixer.music.get_busy():
                mixer.music.play(start = timestamp)
                self.timer.curr_time = timestamp
                mixer.music.pause()
            else:
                mixer.music.set_pos(timestamp)
                self.timer.curr_time = timestamp
                x_loc = 50
                latest_timestamp = timestamp
                

        
                
        #Contains all of the interval buttons (as a replacement for single variables)
        interval_buttons = []

        #The pixel distance from the left side of the line to the left of the canvas
        line_offset = 50
        #The pixel length of the line
        line_length = 400
        i = 0
        for timestamp in self.intervals:
            interval_buttons.append(tk.Button(music_canvas,text = i,
                                              width = 1,height = 2,
                                              command = lambda timestamp = timestamp: play_from(timestamp)))
            
            interval_buttons[i].place(x = line_offset+(timestamp/self.total_time)*400,
                                      y = 75,anchor = tk.CENTER)
            i+=1
            
        '''End of Interval Buttons'''
        
        play_button = tk.Button(music_level,text = 'Play',width = 3,height = 1,
                                     command = self.play)
        play_button.place(relx = 0.5,rely = 0.8,anchor = tk.CENTER)
        
        unpause_button = tk.Button(music_level,text = 'l>',width = 2,height = 1,
                                     command = self.unpause)
        unpause_button.place(relx = 0.525,rely = 0.7,anchor = tk.CENTER)
        
        pause_button = tk.Button(music_level,text = '||',width = 2,height = 1,
                                     command = self.pause)
        pause_button.place(relx = 0.475,rely = 0.7,anchor = tk.CENTER)

        load_button = tk.Button(music_level,text = 'Load',width = 5,height = 1,command = self.load)
        load_button.place(relx = 0.075,rely = 0.075,anchor = tk.CENTER)

        queue_button = tk.Button(music_level,text = 'Queue',width = 5,height = 1,command = lambda: print('Big Chungus'))
        queue_button.place(relx = 0.16,rely = 0.075,anchor = tk.CENTER)

        #Only purpose is to turn off the music and delete the window
        def close_func():
            self.stop()
            print('ran')
            music_level.destroy()
            
            
        close_button = tk.Button(music_level,text = 'Close',width = 10,height = 1,command = close_func)
        close_button.place(relx = 0.9,rely = 0.9,anchor = tk.CENTER)

        tk.Label(music_level,text = self.name,font = ('Ariel',14)).place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)

        music_level.mainloop()

    def to_canvas(self,root):

        #Updates the time by clock var increment_val
        #NOTE: After() accuracy depends on what you run the python on
        def update_timer():
            #print(str(self.timer.curr_time) + f'+{self.timer.increment_value}')
            self.timer.increment()
            time_label.config(text = self.timer)
            time_label.after(500,update_timer)
        
        
        music_canvas = tk.Canvas(root,width = 600,height = 250,bg = 'white')
        #Border for the top layer
        music_canvas.create_rectangle(2,2,600,300,outline = 'black')

        
        timer_canvas = tk.Canvas(music_canvas,width = 500,height = 150,bg = 'white')
        timer_canvas.place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)
        
        #Label to store the current time
        time_label = tk.Label(timer_canvas,text = self.timer)
        time_label.place(relx = 0.8895,rely = 0.9,anchor = tk.CENTER)
        update_timer()
        
        #Border for the timer canvas
        timer_canvas.create_rectangle(2,2,500,150,outline = 'black')

        #Line for the progress bar
        timer_canvas.create_line(50,75,450,75)

        #Progress
        progress_line = timer_canvas.create_line(50,70,50,80)

        def play_from(timestamp):
            
            #If the current song playing isn't the one whose button was clicked, do nothing
            if self.active_mp3 != self.name:
                print('error')
                return
            if not mixer.music.get_busy():
                mixer.music.play(start = timestamp)
                self.timer.curr_time = timestamp
                mixer.music.pause()
            else:
                mixer.music.set_pos(timestamp)
                self.timer.curr_time = timestamp
                
                

        
                
        #Contains all of the interval buttons (as a replacement for single variables)
        interval_buttons = []

        #The pixel distance from the left side of the line to the left of the canvas
        line_offset = 50
        #The pixel length of the line
        line_length = 400
        i = 0
        for timestamp in self.intervals:
            interval_buttons.append(tk.Button(timer_canvas,text = i,
                                              width = 1,height = 2,
                                              command = lambda timestamp = timestamp: play_from(timestamp)))
            
            interval_buttons[i].place(x = line_offset+(timestamp/self.total_time)*400,
                                      y = 75,anchor = tk.CENTER)
            i+=1
            
        '''End of Interval Buttons'''
        
        play_button = tk.Button(music_canvas,text = 'Play',width = 3,height = 1,
                                     command = self.play)
        play_button.place(relx = 0.5,rely = 0.9,anchor = tk.CENTER)
        
        unpause_button = tk.Button(music_canvas,text = 'l>',width = 2,height = 1,
                                     command = self.unpause)
        unpause_button.place(relx = 0.525,rely = 0.7,anchor = tk.CENTER)
        
        pause_button = tk.Button(music_canvas,text = '||',width = 2,height = 1,
                                     command = self.pause)
        pause_button.place(relx = 0.475,rely = 0.7,anchor = tk.CENTER)

        load_button = tk.Button(music_canvas,text = 'Load',width = 5,height = 1,command = self.load)
        load_button.place(relx = 0.075,rely = 0.075,anchor = tk.CENTER)

        
        
        #Only purpose is to turn off the music and delete the window
        def close_func():
            self.stop()
            music_canvas.destroy()
            
            
        close_button = tk.Button(music_canvas,text = 'Close',width = 10,height = 1,command = close_func)
        close_button.place(relx = 0.9,rely = 0.9,anchor = tk.CENTER)

        tk.Label(music_canvas,text = self.name,font = ('Ariel',14)).place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)

        tk.Label(music_canvas,text = f'Author: {self.author}').place(relx = 0.85,rely = 0.1,anchor = tk.CENTER)
        tk.Label(music_canvas,text = self.timer.sec_to_format(self.total_time)).place(relx = 0.825,rely = 0.6,anchor = tk.CENTER)

        return music_canvas
        
        


    print(sauron.total_time)
    
    
