import tkinter as tk
from sys import path

path.insert(0,'../Model')
from music_data import Music

class MusicCanvas:
    
    def __init__(self,root,music):
        self.music_canvas = tk.Canvas(root,width = 600,height = 250,bg = 'white')
        #Border for the top layer
        self.music_canvas.create_rectangle(2,2,600,300,outline = 'black')
        self.music_canvas.pack()

        timer_canvas = tk.Canvas(self.music_canvas,width = 500,height = 150,bg = 'white')
        timer_canvas.place(relx = 0.5,rely = 0.5,anchor = tk.CENTER)

        self.time_label = tk.Label(timer_canvas,text = music.timer)
        self.time_label.place(relx = 0.8895,rely = 0.9,anchor = tk.CENTER)

        #Border for the timer canvas
        timer_canvas.create_rectangle(2,2,500,150,outline = 'black')

        #Line for the progress bar
        timer_canvas.create_line(50,75,450,75)

        #Progress
        progress_line = timer_canvas.create_line(50,70,50,80)

        #Contains all of the interval buttons (as a replacement for single variables)
        self.interval_buttons = []
        #The pixel distance from the left side of the line to the left of the canvas
        line_offset = 50
        #The pixel length of the line
        line_length = 400
        i = 0

        for timestamp in music.intervals:
            self.interval_buttons.append(tk.Button(timer_canvas,text = i,
                                              width = 1,height = 2))
            self.interval_buttons[i].place(x = line_offset+(timestamp/music.total_time)*400,
                                      y = 75,anchor = tk.CENTER)
            i+=1

                                         

        self.play_button = tk.Button(self.music_canvas,text = 'Start',width = 4,height = 1)
                                     #command = self.play)
        self.play_button.place(relx = 0.5,rely = 0.9,anchor = tk.CENTER)

        self.unpause_button = tk.Button(self.music_canvas,text = 'l>',width = 2,height = 1)
                                     #command = self.unpause)
        self.unpause_button.place(relx = 0.525,rely = 0.7,anchor = tk.CENTER)
        
        self.pause_button = tk.Button(self.music_canvas,text = '||',width = 2,height = 1)
                                     #command = self.pause)
        self.pause_button.place(relx = 0.475,rely = 0.7,anchor = tk.CENTER)

        self.load_button = tk.Button(self.music_canvas,text = 'Load',width = 5,height = 1)#,command = self.load)
        self.load_button.place(relx = 0.075,rely = 0.075,anchor = tk.CENTER)

        self.close_button = tk.Button(self.music_canvas,text = 'Close',width = 10,height = 1)#,command = close_func)
        self.close_button.place(relx = 0.9,rely = 0.9,anchor = tk.CENTER)

        tk.Label(self.music_canvas,text = music.name,font = ('Ariel',14)).place(relx = 0.5,rely = 0.075,anchor = tk.CENTER)

        tk.Label(self.music_canvas,text = f'Author: {music.author}').place(relx = 0.85,rely = 0.1,anchor = tk.CENTER)
        tk.Label(self.music_canvas,text = music.timer.sec_to_format(music.total_time)).place(relx = 0.825,rely = 0.6,anchor = tk.CENTER)
        



if __name__ == '__main__':

    root = tk.Tk()

    mu = Music('Crazy','this/path',author = 'Le Serafim',total_time = 120)

    mc = MusicCanvas(root,mu)
