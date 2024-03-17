import csv
import pandas as pd


'''
Example:
criteria = {'age': '25', 'gender': 'Male'}
filtered_data = filter_csv('example.csv', criteria)
'''

def filter_csv(filepath, criteria):
    filtered_rows = []
    with open(filepath, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if all(row[column] == value for column, value in criteria.items()):
                filtered_rows.append(row)
    return filtered_rows

def join_csv(*filepaths) :
  csv_files=[]

  for i in filepaths:
     csv_files.append(i)

  dfs = [pd.read_csv(file) for file in csv_files]

  merged_df = dfs[0]

  for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on='common_column', how='inner')

  return merged_df
     

def aggregate_csv(filepath, col, opr):
    
    df = pd.read_csv(filepath)
    
    if opr == 'sum':
        result = df[col].sum()
    elif opr == 'mean':
        result = df[col].mean()
    elif opr == 'min':
        result = df[col].min()
    elif opr == 'max':
        result = df[col].max()
    return result
    


def format_csv(filepath) :
  pass

def get_csv_cols(filepath) :
  with open(filepath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        column_names = next(reader)
  return column_names
