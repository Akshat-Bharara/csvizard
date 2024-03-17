"""
App to work with CSV files
"""

# csvizard/__init__.py

from rich.console import Console

__app_name__ = "CSVizard"
__version__ = "0.1.0"

console = Console()

(
SUCCESS,
PATH_ERROR,
UNKNOWN_ERROR
)= range(3)

ERRORS = {
  PATH_ERROR : "something is wrong with the file path",
  UNKNOWN_ERROR : "some unknown error occured"
}