import pandas as pd
import pickle

class Data():
    def __init__(self):
        file = self.load()
        self.M = file.display()
    def display(self):
        return self.M
    def merge(self,filename):
        new = upload(filename)
        self.M = pd.concat([new, self.M], axis=0, copy=False)
        self.M = pd.DataFrame.dropna(self.M)
        self.M = self.M.drop_duplicates()
        self.save()
        return self.M
    def save(self):
        index = Index()
        row = index.recent()
        number = row[0]
        name = row[1]
        if self.isduplicate(number):
            index.remove()
        try:
            with open(name + ".pickle", "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
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

def upload(filename):
    df = pd.read_csv(filename, delimiter=';', low_memory=False, decimal=',')
    df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
    df = df.drop(columns=['Time_ms', 'Validity'])
    table = pd.pivot_table(data=df, index=['VarName','TimeString'])
    return table


class Index():
    def __init__(self):
        index = self.load()
        self.M = index.display()
    def add(self,*row):
        if len(row)==0:
            number = input("Project Number (###):")
            name = input("Project Name:")
            row = [int(number),name]
        self.M.append(row)
        self.save()
        return self.M
    def save(self):
        try:
            with open("index.pickle", "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)
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
    def recent(self):
        return self.M[-1]
    def remove(self):
        self.M = self.M[0:-1]
        self.save()
    def display(self):
        return self.M
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




