import pandas as pd
from music_data import Music
import random

class FileWriter:

    def __init__(self):
        self.df = pd.read_csv('../Saving/song_data.csv',
                              names = ['name','path','author','intervals','bpm','total_time','category'])
    def save_df(self,df):
        df.to_csv('../Saving/song_data.csv',index = False,header = False)
        
        

    def save_to_music_array(self):
        
        song_list = MusicArray()

        #Format data into LinkedList
        for row in self.df.itertuples():
            song = Music(row.name,row.path,author = row.author,bpm = row.bpm,
                         total_time = row.total_time)
            #To avoid the csv format from parsing intervals, they are divided by '|'
            intervals = row.intervals.split('|')
            for i in range(len(intervals)):
                intervals[i] = float(intervals[i])
            song.intervals = intervals

            song.bpm = row.bpm
            song.total_time = row.total_time
            
            song.category = row.category

            #Add to the LinkedList
            song_list.add_ordered(song)

        return song_list
        
class Node:
    def __init__(self,song):
        self.song = song
        self.next = None

    def __str__(self):
        return str(self.song)

class LinkedList:
    def __init__(self):
        self.head = None

    def get_head(self):
        return self.head
    

    #Add a node to the end of the linked list
    def add_node(self,node):
        #If LinkedList is empty, make the node the head
        if self.head == None:
            self.head = node
            return
        
        n = self.head
        #Traverse to the end
        while n.next != None:
            n = n.next
        #Add to the chain
        n.next = node
        return

    def add_ordered_node(self,node):
        #If LinkedList is empty, make the node the head
        if self.head == None:
            #print('case1')
            
            self.head = node
            return
        #If the node should be the new head
        elif node.song.compare_to(self.head.song) < 0:
            #print('case2')
            
            node.next = self.head
            self.head = node
            return
        
        #print('case3')
        
        n = self.head
        #Traverse until you reach the end or find the right spot
        while n.next != None and node.song.compare_to(n.next.song) > 0:
            n = n.next
        #Found the spot, now insert the node
        node.next = n.next
        n.next = node
        return

    #Removes the node at position i by cutting it out of the chain
    def remove_index(self,index):
        #Remove the head if index is 0
        
        if index == 0:
            self.head = self.head.next
        else:
            i = 0
            n = self.head
            while n.next != None and i < index-1:
                n = n.next
                i+=1
            #Met the end
            if n.next == None:
                return None
            else:
                #Remove by unlinking from chain
                to_remove = n.next
                n.next = n.next.next
                
                return to_remove
           
    def remove_music(self,song):
        n = self.head
        if n == None:
            return None
        elif n.song == song:
            to_remove = n
            self.head = n.next
            return to_remove
        
        while n.next != None and n.next.song != song:
            n = n.next
        if n.next == None:
            #Do nothing
            return None
        else:
            to_remove = n.next
            n.next = n.next.next
            return to_remove

    def to_df(self):
        data = {'name':[],'path':[],'author':[],'intervals':[],'bpm':[],'total_time':[],'category':[]}
        df = pd.DataFrame(data)

        n = self.head
        while n != None:
            song = n.song

            #Convert intervals into a string again for saving
            intervals = str(song.intervals).replace('[','').replace(']','').replace(',','|').replace(' ','')
            print(intervals)
            data = {'name':[song.name],'path':[song.path],'author':[song.author],'intervals':[intervals],
                    'bpm':[song.bpm],'total_time':[song.total_time],'category':[song.category]}
            new_row = pd.DataFrame(data)
            df = pd.concat([df,new_row],ignore_index = True)
            n = n.next
        return

    #Converts a Linked List to an array of songs
    def to_array(self):
        alist = []
        n = self.head
        while n != None:
            alist.append(n.song)
            n = n.next
        return alist

    #Returns a linked list of the same size, but with songs in a random sequence
    def randomize(self):
        alist = self.to_array()
        #If the queue is of length 1, it cannot be randomized
        if len(alist) <= 1:
            return self
        #Use selection sort, but selecting random elements each time
        for i in range(len(alist)):
            take = random.randint(i,len(alist)-1)
            temp = alist[i]
            alist[i] = alist[take]
            alist[take] = temp

        queue = LinkedList()
        queue.head = Node(alist[0])
        n = queue.head
        for i in range(1,len(alist)):
            n.next = Node(alist[i])
            n = n.next

        return queue

    def replace_head(self,new_head):
        if self.head == None:
            self.head = new_head
            return
        new_head.next = self.head.next
        self.head = new_head
        return
        
    def __str__(self):
        s = ''
        n = self.head
        while n != None:
            s+=str(n) + '\n'
            n = n.next
        return s

class MusicArray:
    def __init__(self):
        self.array = []

    def length(self):
        return len(self.array)
    
    def get(self,index):
        return self.array[index]
    
    #Adds a song to the end of the list
    def add(self,song):
        self.array.append(song)

    #Adds a song to its sorted position
    def add_ordered(self,song):
        i = 0
        while i < self.length() and song.compare_to(self.get(i)) > 0:
            i+=1
        self.array.insert(i,song)

    def remove_index(self,index):
        return self.array.pop(index)

    def remove(self,song):
        return self.array.remove(song)
        
    
        
    def __str__(self):
        
        s = 'Music Array\n'
        for i in range(self.length()):
            s += str(self.get(i)) + '\n'
        return s

    #Converts Array to dataframe format
    def to_df(self):
        data = {'name':[],'path':[],'author':[],'intervals':[],'bpm':[],'length':[],'category':[]}
        df = pd.DataFrame(data)

        for i in range(self.length()):
            song = self.get(i)
            intervals = str(song.intervals).replace('[','').replace(']','').replace(',','|').replace(' ','')
            data = {'name':[song.name],'path':[song.path],'author':[song.author],'intervals':[intervals],
                'bpm':[song.bpm],'length':[song.total_time],'category':[song.category]}
            new_row = pd.DataFrame(data)
            df = pd.concat([df,new_row],ignore_index = True)
            
        return df

    #Returns a list of all Music items that have subsets of both name and category parameters (empty param means the null set, which is a subset of any set)
    #Options for gate: 'and', 'or', 'not'
    def query_to_list(self,name,category,**kwargs):
        gate = kwargs.get('gate','and')
        results = []
        if gate == 'or':
            for song in self.array:
                if name in song.name or category in song.category:
                    results.append(song)
        elif gate == 'not':
            #Ensure that 
            if name == '':
                name = 'Somethingyouwillneverfindinaname854058'
            if category == '':
                category = 'thiswillneverbeacategory478695'
            for song in self.array:
                if name not in song.name and category not in song.category:
                    results.append(song)
        else:
            for song in self.array:
                if name in song.name and category in song.category:
                    results.append(song)
                    
        return results

if __name__ == '__main__':

    fw = FileWriter()
    print(fw.save_to_music_array())
