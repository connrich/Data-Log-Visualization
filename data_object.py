import pandas as pd
import pickle
import os
#Data object for saving pandas dataframes
class Data():
    #initialize by loading file
    def __init__(self):
        file = self.load()
        self.M = file.display()
    #blank function that returns dataframe
    def display(self):
        return self.M
    #merges current data frame with new data, deletes repeats
    def merge(self,filename):
        df = pd.read_csv(filename, delimiter=';', low_memory=False, decimal=',')
        df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
        df = df.drop(columns=['Time_ms', 'Validity'])
        table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])
        self.M = pd.concat([table, self.M], axis=0, copy=False)
        self.M = pd.DataFrame.dropna(self.M)
        self.M = self.M.drop_duplicates()
        self.M.sort_values(by="TimeString", inplace=True)
        self.M = pd.pivot_table(data=self.M, index=['VarName', 'TimeString'])
        self.save()
        os.remove(filename)
        return self.M
    #saves dataframe
    def save(self):
        index = Index()
        row = index.recent()
        number = row[0]
        name = row[1]
        if index.isduplicate(number):
            index.remove()
        try:
            with open(name + ".pickle", "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
    #loads dataframe
    def load(self):
        number = input("Project Number (###):")
        index = Index()
        name = index.search(int(number))
        index.add([int(number), name])
        try:
            with open(name+'.pickle', "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported): ", ex)
    #returns name of dataframe
    def name(self):
        index = Index()
        row = index.recent()[1]
        return row
    #sorts dataframe by date
    def sort(self):
        self.M.sort_values(by="TimeString", inplace=True)
        self.M = pd.pivot_table(data=self.M, index=['VarName', 'TimeString'])
        self.save()


#index object for pickling that stores project numbers and names (called by Data() above)
class Index():
    #initializes index
    def __init__(self):
        index = self.load()
        self.M = index.display()
    #adds row to index
    def add(self,*row):
        if len(row)==0:
            number = input("Project Number (###):")
            name = input("Project Name:")
            row = [int(number),name]
        self.M.append(row)
        self.save()
        return self.M
    #saves index
    def save(self):
        try:
            with open("index.pickle", "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
    #loads index
    def load(self):
        try:
            with open('index.pickle', "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported): ", ex)
    def search(self,number):
        row = []
        for r in self.M:
            for c in r:
                if c == number:
                    row = r
                    break
        if len(row)>0:
            return row[1]
        if len(row)==0:
            name = input("Project Number")
            self.add(number, name)
            return name
    #returns the last row
    def recent(self):
        row = self.M[-1]
        row = row[0]
        return row
    #removes the last row
    def remove(self):
        self.M = self.M[0:-1]
        self.save()
    #returns the index
    def display(self):
        return self.M
    #checks for duplicates in the index, returns true if there are duplicates
    def isduplicate(self,number):
        store = 0
        for r in self.M:
            for c in r:
                if c == number:
                    store+=1
        if store ==1:
            return False
        if store ==2:
            return True




