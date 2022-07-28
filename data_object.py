import pandas as pd
import pickle
import os
#Data object for saving pandas dataframes
class Data():
    #initialize by loading file
    def __init__(self, number):
        self.number = number
        self.index = self.loadindex()
        file = self.load()
        self.saveindex()
        if file is None:
            filename = input("File Name: ")
            df = pd.read_csv(filename, delimiter=';', low_memory=False, decimal=',')
            df = pd.DataFrame.dropna(df)
            df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
            self.M = df.drop(columns=['Time_ms', 'Validity'])
            self.name = input("Project Name:")
            self.index.append([number, self.name])
            self.saveindex()
            self.save()
            os.remove(filename)
        else:
            self.M = file
            self.save()
    #blank function that returns dataframe
    def display(self):
        return self.M
    def dispindex(self):
        return self.index
    def pivot(self):
        return pd.pivot_table(data=self.M, index=['VarName', 'TimeString'])
    def clean(self):
        self.M = pd.DataFrame.dropna(self.M)
        self.M = self.M.drop_duplicates(subset = ['TimeString','VarName'])
        self.M.sort_values(by="TimeString", inplace=True)
        self.save()
        return self.M
    #merges current data frame with new data, deletes repeats
    def merge(self,filename):
        df = pd.read_csv(filename, delimiter=';', low_memory=False, decimal=',')
        df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
        df = df.drop(columns=['Time_ms', 'Validity'])
        self.M = pd.concat([df, self.M], axis=0, copy=False)
        self.clean()
        os.remove(filename)
        self.save()
        return self.M
    #saves dataframe
    def save(self):
        try:
            with open(self.name + ".pickle", "wb") as f:
                pickle.dump(self.M, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
    #loads dataframe
    def saveindex(self):
        try:
            with open("index.pickle", "wb") as f:
                pickle.dump(self.index, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
    def load(self):
        self.loadindex()
        self.name = self.search()
        if self.name is None:
            return None
        else:
            try:
                with open(self.name+'.pickle', "rb") as f:
                    return pickle.load(f)
            except Exception as ex:
                print("Error during unpickling object (Possibly unsupported): ", ex)
    def loadindex(self):
        try:
            with open('index.pickle', "rb") as f:
                return pickle.load(f)
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported): ", ex)

    #returns name of dataframe
    def search(self):
        for r in self.index:
            if r[0] == self.number:
                return r[1]
        return None
    def sort(self):
        self.M.sort_values(by="TimeString", inplace=True)
        self.M = pd.pivot_table(data=self.M, index=['VarName', 'TimeString'])
        self.save()
