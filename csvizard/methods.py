import csv
import pandas as pd

"""
(col [=|!=|>|<|>=|<=] value [&/||/])*
"""

def filter_csv(filepath, conditions) :
  df = pd.read_csv(filepath)
  mask = pd.Series([True] * len(df))
  conditions_list = []

  for cond in conditions.split("&"):
    conditions_list.extend(cond.split("||"))
  
  for cond in conditions_list:
    parts = cond.strip().split()

    if len(parts) != 3:
      raise ValueError("Invalid condition format")
    
    col, operator, value = parts
    
    try:
      value = float(value)
    except ValueError:
      try:
        value = int(value)
      except ValueError:
        pass
    
    if operator == "=":
      mask &= df[col] == value
    elif operator == "!=":
      mask &= df[col] != value
    elif operator == ">":
      mask &= df[col] > value
    elif operator == "<":
      mask &= df[col] < value
    elif operator == ">=":
      mask &= df[col] >= value
    elif operator == "<=":
      mask &= df[col] <= value
    else:
      raise ValueError("Invalid operator")

  filtered_df = df[mask]
  
  return filtered_df

def join_csv(*filepaths) :
  csv_files=[]

  for i in filepaths:
    csv_files.append(i)

  dfs = [pd.read_csv(file) for file in csv_files]

  merged_df = dfs[0]
  
  common_columns = set(dfs[0].columns)
  for df in dfs[1:]:
    common_columns = common_columns.intersection(df.columns)
  
  if len(common_columns) == 0:
    raise ValueError("No common columns found")

  for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on=[*common_columns], how='inner')

  return merged_df

def aggregate_csv(filepath, col, opr):
  df = pd.read_csv(filepath)
  result = None

  match opr :
    case "sum" :
      result = df[col].sum()
    case "avg" :
      result = df[col].mean()
    case "min" :
      result = df[col].min()
    case "max" :
      result = df[col].max()

  return result

def format_csv(filepath) :
  pass

def get_csv_cols(filepath) :
  with open(filepath, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    column_names = next(reader)

  return column_names
