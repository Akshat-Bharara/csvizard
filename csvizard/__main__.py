"""
App Entry-point
"""

# csvizard/__main__.py

import pandas as pd
from csvizard import __app_name__, console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from rich.console import Console
from rich.progress import Progress
import typer
from pyfiglet import Figlet
from pathlib import Path
from time import sleep
from random import randint

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
  opr = ["Exit", "Filter", "Join", "Aggregate", "Manage files", "View CSV", "Bored..."]
  
  for i, o in enumerate(opr) : cons.print(i, o)

  return Prompt.ask("Enter operation number", choices=[str(o) for o in range(len(opr))], default="0")

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

  if len(csv_paths) < 1 :
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
      console.print(f"Selected file: [green]{csv_paths[file_idx]}")
      console.print(get_csv_cols(csv_paths[file_idx]))
      cond = Prompt.ask("Query [pink]\[(col [=|!=|>|<|>=|<=] value [&||| ])*\]")

      try :
        df = filter_csv(csv_paths[file_idx], cond)
        console.print(df.head())
        gen_ch = Confirm.ask("Generate CSV ?")
        
        if gen_ch :
          gen_csv(df)
          console.print(f"[green]Generated successfully!")
      except :
        console.print("[red]Invalid condition")
        Prompt.ask("Press any key to go back")
        return main()
      
      Prompt.ask("Press any key to go back")
      main()
      
    case 2 :      
      if (len(csv_paths) < 2) : 
        console.print("[red]There should atleast be 2 files to perform join !")
        sleep(1)
        return main()

      console.clear()
      show_files()

      file_idxs = Prompt.ask("Select files", default=0).split()

      try :
        console.print("Selected files :")
        for i in file_idxs :  console.print("[green]" + csv_paths[int(i)])
      except :
        console.print("[red]Enter valid indices!")
        sleep(1)
        return main()
      
      with Progress() as progress:
        task1 = progress.add_task("[green]Working...", total=1000)

        while not progress.finished:
            progress.update(task1, advance=1.3 + randint(2, 7))
            sleep(0.02)

      joint_df = join_csv(*[csv_paths[int(i)] for i in file_idxs])
      console.print(joint_df)
      ch_gen = Confirm.ask("Generate a CSV file ?")
      
      if ch_gen :
        gen_csv(joint_df)
      
      Prompt.ask("Press any key to go back")
      main()
      
    case 3 :
      opr_choices = ["sum", "avg", "min", "max"]
      show_files()
      file_idx = Prompt.ask("Select file", choices=[int(i) for i in range(len(csv_paths))], default=0) if len(csv_paths) > 1 else 0
      file_path = csv_paths[file_idx]
      cols = get_csv_cols(file_path)
      opr = Prompt.ask("Select operation", choices=opr_choices)
      col = Prompt.ask("Select column", choices=cols)
      result = aggregate_csv(file_path, col, opr)
      console.print(result)
      Prompt.ask("Press any key to go back")
      main()

    case 4 :
      console.clear()
      show_files()
      opr = Prompt.ask("Select operation", choices=["add", "rm"], default="cancel")

      if opr == "add" :
        add_files(prompt_files())
      elif opr == "rm" :
        file_idxs = Prompt.ask("Enter file indexes to remove").split()
        file_idxs = [int(i) for i in file_idxs]

        try :
          console.print("Files removed")
          
          for i in range(len(csv_paths)) :
            if i in file_idxs :
              console.print(f"[red]{i} {csv_paths[i]}")

          new_list = [csv_paths[i] for i in range(len(csv_paths)) if i not in file_idxs]
          csv_paths.clear()
          csv_paths.extend(new_list)
        except :
          console.print("[red]Invalid index(es)!")

      else :
        pass

      Prompt.ask("Press any key to go back")
      main()
    
    case 5 :
      show_files()
      file_idx = Prompt.ask("Select file", choices=[str(i) for i in range(len(csv_paths))], default=0) if len(csv_paths) > 1 else 0
      file_path = csv_paths[int(file_idx)]
      df = pd.read_csv(file_path)

      with console.pager() :
        console.print(df)
      
      Prompt.ask("Press any key to go back")
      main()
    
    case 6 :
      console.clear()
      print_title()
      console.print("Let's play a game...")
      sleep(1)
      console.print("The computer has picked a number between 1 and 1000")
      sleep(1)
      console.print("You have 10 tries to guess, Good luck!")
      sleep(1)
      console.print("\n")
      num = randint(1, 1000)

      for i in range(10) :
        if i == 9 :
          console.print(f"[red]Last try !")

        ch = int(Prompt.ask(f"Trial {i + 1}"))

        if ch == num :
          console.print("[green]gg wp !")
          Prompt.ask("Press any key to continue")
          return main()
        elif ch < num :
          console.print("[blue]go higher")
        else :
          console.print("[blue]go lower")

      console.print(f"\n[red bold]moye moye")
      console.print(f"the number was {num}")
      Prompt.ask("Press any key to go back")
      main()


if __name__ == "__main__":
  typer.run(main)

# C:\Scripts\csvizard\.gitignore C:\Scripts\csvizard\csvizard\cli.py C:\Scripts\csvizard\cli.py