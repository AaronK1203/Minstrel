import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

mixer.init()

def kill_mixer():
    mixer.quit()

pre_path = '../Saving/'

class Music:

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
            
    def load(self):
        mixer.music.load(f'{pre_path}{self.path}')
        self.active_mp3 = self.name
        self.timer.curr_time = 0
        self.timer.increment_value = 0

    def play(self):
        mixer.music.load(f'{pre_path}{self.path}')
        mixer.music.play()
        self.timer.curr_time = 0
        self.timer.increment_value = 0.5
    
    '''
    def play_from(self,timestamp):
        mixer.set_pos(timestamp)
        self.timer.curr_time = timestamp
    '''

    def play_from(self,timestamp):
            
        #If the current song playing isn't the one whose button was clicked, do nothing
        if self.active_mp3 != self.name:
            print('error: song isn\'t loaded')
            return
        if not mixer.music.get_busy():
            mixer.music.play(start = timestamp)
            self.timer.curr_time = timestamp
            mixer.music.pause()
        else:
            mixer.music.set_pos(timestamp)
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

class Clock:
    def __init__(self,start):
        self.curr_time = start
        #Records the number by which to increment for each update
        self.increment_value = 0

    #formats param seconds to hour:minute:second format
    def sec_to_format(self,seconds):
        hours = seconds//3600
        minutes = (seconds%3600)//60
        seconds = seconds % 60

        hours_str = str(int(hours))
        minutes_str = str(int(minutes))
        seconds_str = str(int(seconds))

        if hours < 10:
            hours_str = '0'+hours_str
        if minutes < 10:
            minutes_str = '0'+minutes_str
        if seconds < 10:
            seconds_str = '0'+seconds_str
        return f'{hours_str}:{minutes_str}:{seconds_str}'
    
    #Formats curr time to hour:minute:second format
    def to_format(self):
        return self.sec_to_format(self.curr_time)

    def __str__(self):
        return self.to_format()

    #Increments current time by time parameter
    def increment_by(self,time):
        self.curr_time += time

    def increment(self):
        self.increment_by(self.increment_value)
