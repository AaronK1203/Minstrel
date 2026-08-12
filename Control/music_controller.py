import tkinter as tk
from sys import path

path.insert(0,'../Model')
path.insert(0,'../View')

from music_view import MusicCanvas
from music_data import Music

def bind_button(button,command):
    button.configure(command = command)

class MusicController:

    def __init__(self,music):
        self.music = music
        self.mc = None

    def create_canvas(self,root):
        self.mc = MusicCanvas(root,self.music)
        
        bind_button(self.mc.close_button,self.close_func)

        bind_button(self.mc.play_button,self.music.play)
        bind_button(self.mc.pause_button,self.music.pause)
        bind_button(self.mc.unpause_button,self.music.unpause)
        bind_button(self.mc.load_button,self.music.load)
        
        
        
        i = 0
        for timestamp in self.music.intervals:
            #bind_button(self.mc.interval_buttons[i],
                        #lambda time=timestamp: self.music.play_from(time))
            self.mc.interval_buttons[i].configure(command = lambda time=timestamp: self.music.play_from(time))
            i+=1

        self.update_timer()

        return self.mc

        
    #Updates the time by clock var increment_val
    #NOTE: After() accuracy depends on what you run the python on
    def update_timer(self):
        #print(str(self.timer.curr_time) + f'+{self.timer.increment_value}')
        self.music.timer.increment()
        self.mc.time_label.config(text = self.music.timer)
        self.mc.time_label.after(500,self.update_timer)
    

    #Only purpose is to turn off the music and delete the window
    def close_func(self):
        self.music.stop()
        self.mc.music_canvas.destroy()

    
        

        
        
if __name__ == '__main__':

    root = tk.Tk()

    mu = Music('Seliana','mp3_files/Seliana-Theme.mp3',author = 'MHW',total_time = 120)
    mu.intervals = [0.0,50.0]

    mc = MusicController(mu)
    mc.create_canvas(root)
