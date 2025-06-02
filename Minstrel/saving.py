import pandas as pd
from music import Music


def read_save():
    df = pd.read_csv('save_data/song_data.csv',
                 names = ['name','path','intervals','bpm','length','category'])
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
        song = Music(row.name,row.path,bpm = row.bpm,length = row.length)
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
    data = {'name':[],'path':[],'intervals':[],'bpm':[],'category':[]}
    df = pd.DataFrame(data)

    n = alist.head
    while n != None:
        song = n.song

        #Convert intervals into a string again for saving
        intervals = str(song.intervals).replace('[','').replace(']','').replace(',','|').replace(' ','')
        print(intervals)
        data = {'name':[song.name],'path':[song.path],'intervals':[intervals],
                'bpm':[song.bpm],'category':[song.category]}
        new_row = pd.DataFrame(data)
        df = pd.concat([df,new_row],ignore_index = True)
        n = n.next

    save_df(df)
        

def save_df(df):
    df.to_csv('save_data/song_data.csv',index = False,header = False)


if __name__ == '__main__':

    
    print()
    

    
