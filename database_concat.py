import pandas as pd



# BOM for a specific project
# sheet_name = the name of the sheet containing the BOM
# header = index for the row containing the headers 
bom_path = "G:\\Shared drives\\General\\QTC\\Manufacturing\\P638 University of Buffalo\\02. Project Docs\\P638 University of Buffalo - Project Doc 20220419 EJ.xlsx"
project_number = bom_path.split("\\")[-1][1:4]
project_bom = pd.read_excel(bom_path, 
                            sheet_name="BOM", 
                            header=6)

# Remove unneeded columns
project_bom.drop(['Tot (CAD)'], axis=1, inplace=True)
# Make all column headers lower case for consistency
project_bom.rename({name: name.lower() for name in project_bom.columns}, axis=1, inplace=True)
# Remove completely empty rows
project_bom.dropna(how='all', inplace=True)
# Remove rows with a section tag 
# project_bom = project_bom[project_bom['section'].isnull()]

# Reset index after removing all unrelevant rows
project_bom.reset_index()

print(project_bom.iloc[0])




###########################################################

db_path = "G:\\Shared drives\\General\\QTC\\Manufacturing\\P698 - Database\\BackUps\\testversion_p698_database.xlsx"

# Create output dataframe
db_headers = ["id", "c", "part", "vp1", "up1", "vp2", "up2", "desc", "sup", "mfg", "pn", "proj", "sec", "dwg", "dwg_id", "qty", "spare", "po", "resp", "ord", "wk", "s", "each", "d", "n", "l", "b", "w", "upd", "lc"]
output_df = pd.DataFrame(columns=db_headers)

# Map columns to the ouput data frame
output_df['desc'] = project_bom['item description']
output_df['sup'] = project_bom['supplier / manufacturer']
output_df['mfg'] = project_bom['mfg']
output_df['pn'] = project_bom['p/n']
output_df['proj'] = project_number
output_df['dwg_id'] = project_bom['id']
output_df['qty'] = project_bom['qty']
output_df['po'] = project_bom['po']
output_df['s'] = project_bom['stat']
output_df['wk'] = project_bom['lead time (wks)']
output_df['resp'] = project_bom['responsible']
output_df['each'] = project_bom['each (cad)'].fillna(project_bom['usd'])
output_df['d'] = ['U' if pd.isna(x) else 'C' for x in project_bom['each (cad)']]

# Reset the index of the dataframe 
output_df.reset_index(drop=True, inplace=True)

# Populate some columns based on part numbers
cols = ['c', 'part', 'vp1', 'up1', 'vp2', 'up2']

# Concatenate all current sheets into a 'mega' database 
main_db = pd.read_excel(db_path, None)
main_db.pop("400-500's")
main_db = pd.concat(main_db.values())

# Grab part numbers and populate output dataframe based on other sheets
for idx, pn in enumerate(output_df['pn']):
    if not pd.isna(pn):
        # Find another example of the same part 
        try:
            old_part = main_db.loc[main_db['pn'] == pn].iloc[0]
            for col in cols:
                output_df.at[idx, col] = old_part[col]
        except:
            print(f'part at {idx} could not be populated: {pn}')
            pass



# Write dataframe to xlsx
with pd.ExcelWriter(db_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    output_df.to_excel(writer, sheet_name=str(project_number), index=False)