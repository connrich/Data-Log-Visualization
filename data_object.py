import pandas as pd
import pickle

class Data():
    def __init__(self):
        self.M = upload()
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
        try:
            with open("utrecht" + ".pickle", "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported): ", ex)

def upload(filename):
    df = pd.read_csv(filename, delimiter=';', low_memory=False, decimal=',')
    df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')
    df = df.drop(columns=['Time_ms', 'Validity'])
    table = pd.pivot_table(data=df, index=['VarName','TimeString'])
    return table
def load():
    try:
        with open('utrecht.pickle', "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported): ", ex)



