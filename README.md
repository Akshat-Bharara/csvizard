# Ctrl+Alt+Defeat_WEB

WEB - CSVizard : Command Line Tool for performing transformations on CSV files.

### Basic video demo: [https://drive.google.com/file/d/15p63P-F6fwKmx65y7zTLWKAvPBrb5iQG/view?usp=sharing](https://drive.google.com/file/d/1atAlQV8MUEEfuH-ZFF9J9ntGSXvvhS_l/view?usp=drive_link)


## To run the CLI app 

```
pip install -r requirements.txt
python -m csvizard
```


## Technologies Used
- Python
- Typer
- Rich
- Pandas
- csv

## List of Implemented Features

- Implemented an aesthetic UI with an elegant interface
- CLI app that inputs CSV files performs user-specified transformations like filtering, joining, aggregating, and outputs the transformed data to a new CSV file
- Input: The CLI accepts one or more CSV files as input through interactive prompts
- Filtering: Selecting specific rows based on criteria like column values
- Joining: Merging data from multiple CSV files based on the common columns.
- Aggregating: Performing calculations like sum, average, minimum, or maximum on numerical columns.
- The transformed data is written to a new CSV file
- Handling different CSV formats: The CLI handles variations in CSV files, such as delimiters and quoting styles
- Error handling: The tool gracefully handles errors like invalid file paths, missing columns, or out of bound indexes, data type checking during transformation

### Resources
- https://rich.readthedocs.io/en/stable/
- https://typer.tiangolo.com/
