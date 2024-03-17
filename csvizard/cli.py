import typer as tp
from typing import Optional
from csvizard import __app_name__, __version__

app = tp.Typer()

def _version_callback(value: bool) -> None:
  if value:
    tp.echo(f"{__app_name__} v{__version__}")
    raise tp.Exit()
  
@app.callback()
def main(
  version: Optional[bool] = tp.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
  )
) -> None :
  return