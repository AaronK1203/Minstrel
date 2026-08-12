import pandas as pd
from pathlib import Path

#Reads and writes to playlists.csv to keep track of playlists
class LoadScreenModel:
    
    def __init__(self):
        
        self.df = self.save_to_df()

    #Returns a dataframe of the data inside of playlist.csv
    def save_to_df(self):
        df = pd.read_csv('../Saving/playlists.csv',
                        names = ['name','path'])
        return df

    #Given a dataframe, saves the information to playlist.csv
    #(Trigger this method every time the load screen is closed)
    def df_to_save(self,df):
        df.to_csv('../Saving/playlists.csv',index=False,header=False)

    #Creates a new csv file and adds the information to the dataframe
    #Prerequisite: path is unique among all other file names (check in control)
    def create_csv(self,name,path):
        #Create empty dataframe
        empty_df = pd.DataFrame({'name': [],'path': [],'author': [],
                                 'intervals': [],'bpm': [],'total_time':[],
                                 'category':[]})
        #Write to new file
        empty_df.to_csv(f'../Saving/Playlists/{path}',index=False)

        #Add file info to dataframe
        self.df.loc[len(self.df)]=[name,path]

    #Edits the name of a cvs file and updates the dataframe accordingly
    def edit_csv(self,index,name,path):
        #Get original file name and path
        orig_name = self.df.iloc[index,0]
        orig_path = self.df.iloc[index,1]
        #Edit file
        file = Path(f'../Saving/Playlists/{orig_path}')
        file.rename(f'../Saving/Playlists/{path}')

        #Change the dataframe
        self.df.iloc[index] = [name,path]

    #Deletes a csv file and updates the dataframe accordingly
    def delete_csv(self,index):
        #Get the file name
        file_path = self.df.iloc[index,1]
        name = self.df.iloc[index,0]
        #Delete the file
        Path(f'../Saving/Playlists/{file_path}').unlink(missing_ok=True)
        #Delete the dataframe row
        self.df = self.df[self.df['name'] != name]
