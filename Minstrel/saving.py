import pandas as pd
from music import Music


def read_save():
    df = pd.read_csv('save_data/song_data.csv',
                 names = ['name','path','author','intervals','bpm','total_time','category'])
    return df



#Nodes to make LinkedList of songs
class Node:
    def __init__(self,song):
        self.song = song
        self.next = None

    def __str__(self):
        return str(self.song)

class Linked_List:
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
    def remove_index(index):
        #Remove the head if index is 0
        if index == 0:
            self.head = self.head.next
        else:
            i = 0
            n = self.head
            while n.next != None and i < index-1:
                n = n.next
            #Met the end, so not remove anything
            if n.next == None:
                return None
            else:
                #Remove by unlinking from chain
                to_remove = n.next
                n.next = n.next.next
                return to_remove
           
    def remove_music(song):
        n = self.head
        while n != None and n.nxst.song != song:
            n = n.next
        if n == None:
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
        

def save_to_linked_list():

    df = read_save()
    song_list = Linked_List()

    #Format data into LinkedList
    for row in df.itertuples():
        song = Music(row.name,row.path,author = row.author,bpm = row.bpm,length = row.length)
        #To avoid the csv format from parsing intervals, they are divided by '|'
        intervals = row.intervals.split('|')
        for i in range(len(intervals)):
            song.intervals.append(float(intervals[i]))
        
        song.category = row.category

        #Add to the LinkedList
        n = Node(song)
        song_list.add_ordered_node(n)

    return song_list

#Converts a linked list to a df, then saves it
def linked_list_to_save(alist):
    data = {'name':[],'path':[],'author':[],'intervals':[],'bpm':[],'total_time':[],'category':[]}
    df = pd.DataFrame(data)

    n = alist.head
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

    save_df(df)
    
#This will be the class used to store each song
class Music_Array:
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
        s = ''
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
                name = 'Somethingyouwillneverfindinaname'
            if category == '':
                category = 'thiswillneverbeacategory'
            for song in self.array:
                if name not in song.name and category not in song.category:
                    results.append(song)
        else:
            for song in self.array:
                if name in song.name and category in song.category:
                    results.append(song)
                    
        return results





    
            
def save_to_music_array():
    df = read_save()
    song_list = Music_Array()

    #Format data into LinkedList
    for row in df.itertuples():
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

    

def save_df(df):
    df.to_csv('save_data/song_data.csv',index = False,header = False)


if __name__ == '__main__':

    
    alist = Music_Array()
    
    sauron = Music('Sauron','mp3_files/Sauron.mp3',author = 'Bear McCreary',
                   total_time = 165,intervals = [0.0,81.5,100.0],
                   category = 'Battle/Interlude')
    
    mars = Music('Mars - the Bringer of War','mp3_files/Mars-the-Bringer-of-War.mp3',author = 'Gustav Holst',total_time = 425,intervals = [0.0,248.5],
                 category = 'Battle/Sol')
    lacrimosa = Music('Lacrimosa','mp3_files/Lacrimosa-Epic_Version-(Mozart).mp3',category = 'Battle/Victoria',author = 'Samuel Kim')
    lacrimosa.total_time = 175
    psalm135 = Music('Psalm 135','mp3_files/Psalm-135.mp3',category = 'Ambient/Choir',author = 'Andre Serba',total_time = 227)
    thor = Music('The Hammer of Thor','mp3_files/The-Hammer-of-Thor.mp3',author = 'Bear McCreary',category = 'Battle/Nordenskjold',total_time = 202)
    revan = Music('Darth Revan Cover','mp3_files/Darth-Revan-Cover.mp3',author = 'Samuel Kim',category = 'Battle/Beowulf')
    revan.total_time = 172
    deus = Music('Deus in Audiutorium','mp3_files/Deus-in-Adiutorium.mp3',author = 'Clamavi de Profundis',category = 'Ambient/Wondering')
    deus.total_time = 287
    we_praise = Music('We Praise Thee','mp3_files/We-Praise-Thee.mp3',category = 'Misc/Somber',author = 'Pavel Chesnokov',total_time = 218)
    eternal = Music('Eternal Council','mp3_files/Eternal-Counsel-Op40-No2.mp3',category = 'Misc/Somber',author = 'Pavel Chesnokov',total_time = 236)
    
    alist.add_ordered(mars)
    alist.add_ordered(sauron)
    alist.add_ordered(psalm135)
    alist.add_ordered(lacrimosa)
    alist.add_ordered(thor)
    alist.add_ordered(revan)
    alist.add_ordered(deus)
    alist.add_ordered(we_praise)
    alist.add_ordered(eternal)
    alist.add_ordered(line)
    
    #print(alist)

    save_df(alist.to_df())

    clist = save_to_music_array()

    blist = Linked_List()
    n0 = Node(sauron)
    n1 = Node(mars)
    n2 = Node(lacrimosa)

    blist.add_node(n0)
    blist.add_node(n1)
    blist.replace_head(n2)
    #print(blist)

    for song in clist.query_to_list('',''):
        print(song)

    

    
    
    
    
