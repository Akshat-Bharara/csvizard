"""
App Entry-point
"""

# app/__main__.py

from csvizard import cli, __app_name__, console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.tree import Tree
from rich.console import Console
import typer
from pyfiglet import Figlet

csv_paths = []

def prompt_files() :
  return Prompt.ask("Enter CSV file path(s) ").split()

def print_menu() :
  cons = Console(style="blue")
  opr = ["Exit", "Filter", "Join", "Aggregate", "Format"]
  
  for i, o in enumerate(opr) : cons.print(i, o)

  return Prompt.ask("Enter operation number ", choices=[str(o) for o in range(len(opr))], default="0")

def main():
  global csv_paths
  text = Figlet(font="slant", justify="center")
  console.print(Panel(text.renderText(__app_name__), title="Welcome!", border_style="red", title_align="center"))
  csv_paths = prompt_files()

  #  check for csv here

  choice = int(print_menu())

  match choice :
    case 1 :
      console.print("first case")
      
    case 2 :
      console.print("second case")
    
    case _ :
      console.print(choice)


if __name__ == "__main__":
  typer.run(main)