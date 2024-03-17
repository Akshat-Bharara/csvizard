"""
App Entry-point
"""

# csvizard/__main__.py

from csvizard import __app_name__, console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich.console import Console
import typer
from pyfiglet import Figlet
from pathlib import Path
from time import sleep

from csvizard.methods import filter_csv, join_csv, aggregate_csv, format_csv, get_csv_cols

csv_paths = []

def print_title() :
  text = Figlet(font="slant", justify="center")
  console.print(Panel(text.renderText(__app_name__), title="Welcome!", border_style="red", title_align="center"))

def prompt_files() :
  return Prompt.ask("Enter CSV file path(s) ").split()

def add_files(paths) :
  for path in [*paths] :
    if Path(path).exists() :
      if not path.endswith(".csv") :
        console.print(f"[red][bold]{path}[/] not a CSV file")
        continue

      if path in csv_paths :
        console.print(f"[blue]{path} already added")
      else :
        csv_paths.append(path)
        console.print(f"[green][bold]{path}[/] added")

    else :
      paths.remove(path)
      console.print(f"[red][bold]{path}[/] not found")

def print_menu() :
  cons = Console(style="blue")
  opr = ["Exit", "Filter", "Join", "Aggregate", "Format"]
  
  for i, o in enumerate(opr) : cons.print(i, o)

  return Prompt.ask("Enter operation number ", choices=[str(o) for o in range(len(opr))], default="0")

def show_files() :
  for i, path in enumerate(csv_paths) :
    path = Path(path)
    name = path.name
    display_name = name + (f" [white]({path.parent})" if len([*filter(lambda path : Path(path).name == name, csv_paths)]) > 1 else "")
    console.print(f"{i} [blue]{display_name}[/]")

def gen_csv(df) :
  filename = "out.csv"
  delim = Prompt.ask("Delimiter", choices=[",", "|", ":"], default=",")
  filename = Prompt.ask("File name", default="out.csv")
  df.to_csv(filename, sep=delim,index=False)

def main():
  console.clear()
  print_title()
  add_files(prompt_files())

  if len(csv_paths) == 0 :
    sleep(1)
    return main()

  choice = int(print_menu())

  match choice :
    case 1 :
      console.clear()
      show_files()
      file_idx = Prompt.ask("Select file ", choices=[str(i) for i in range(len(csv_paths))], default=0) if len(csv_paths) > 1 else 0
      file_idx = int(file_idx)
      console.print(f"[green]{csv_paths[file_idx]}")
      cond = Prompt.ask("Query [pink]\[(col [=|!=|>|<|>=|<=] value [&||| ])*\]")

      df = filter_csv(csv_paths[file_idx], cond)
      console.log(df.head())
      gen_ch = Confirm.ask("Generate CSV ?")

      if gen_ch : gen_csv(df)
      
    case 2 :      
      if (len(csv_paths) < 2) : 
        console.print("[red]There should atleast be 2 files to perform join !")
        sleep(1)
        return main()

      console.clear()
      show_files()

      file_idxs = Prompt.ask("Select files ", default=0).split()

      try :
        console.print("Selected files :")
        for i in file_idxs :  console.print("[green]" + csv_paths[int(i)])
      except :
        console.print("[red]Enter valid indices!")
        sleep(1)
        main()
      
      joint_df = join_csv(*[csv_paths[int(i)] for i in file_idxs])
      console.print(joint_df)
      ch_gen = Confirm.ask("Generate a CSV file ?")
      
      if ch_gen :
        gen_csv(joint_df)
      
    case 3 :
      opr_choices = ["sum", "avg", "min", "max"]
      show_files()
      file_idx = Prompt.ask("Select file", choices=[str(i) for i in range(len(csv_paths))], default=0) if len(csv_paths) > 1 else 0
      file_path = csv_paths[file_idx]
      cols = get_csv_cols(file_path)
      opr = Prompt.ask("Select operation", choices=opr_choices)
      col = Prompt.ask("Select column", choices=cols)
      result = aggregate_csv(file_path, col, opr)
      console.print(result)

    case 4 :
      show_files()
      file_idx = Prompt.ask("Select file", choices=[str(i) for i in range(len(csv_paths))], default=0) if len(csv_paths) > 1 else 0
      file_idx = int(file_idx)
      console.print(csv_paths[file_idx])

if __name__ == "__main__":
  typer.run(main)

# C:\Scripts\csvizard\.gitignore C:\Scripts\csvizard\csvizard\cli.py C:\Scripts\csvizard\cli.py