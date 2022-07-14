import pandas as pd
import sys
import csv


# Loads the csv and formats ',' to '.' to avoid issues in Excel
def clean_data(args):
    # 1st argument should be path to CSV
    csv_path = args[1]
    df = pd.read_csv(csv_path, header=None, names=[0,1,2,3,4], delimiter=';', low_memory=False)
    
    # Replace commas with decimal point
    df[2] = df[2].apply(lambda x: str(x).replace(',', '.'))
    df[4] = df[4].apply(lambda x: str(x).replace(',', '.'))



    # 2nd argument is path to save location
    if len(args) == 3:
        # Use save location if provided
        df.to_csv(args[2], index=False, header=False)
    else:
        # Overwrite the original data if no location provided
        df.to_csv(args[1], index=False, header=False)


# Concatenates each row together and stores in 1st column
def combineColumns(df: pd.DataFrame) -> pd.Series:
    # Iterate through columns in CSV
    for col in df.columns:
        # Convert NaN to empty string
        df[col] = df[col].fillna('')
        # Skip 1st column
        if col == 0:
            continue
        # Concatenate the column to the first column
        df[0] = df[0].astype(str) + ';' + df[col].astype(str)

    # Discard extraneous columns
    df = df[0]
    # Strip extra ';' that get appended
    df = df.apply(lambda x: x.rstrip(';'))

    return df

if __name__ == '__main__':
    clean_data(sys.argv)