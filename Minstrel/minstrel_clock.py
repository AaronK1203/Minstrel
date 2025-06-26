

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


if __name__ == '__main__':

    clock0 = Clock(0)
    
    resp = ''
    
    while resp == '':
        print(clock0)
        clock0.increment_by(100)

        resp = input()
    
