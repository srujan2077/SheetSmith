# SheetSmith

A Python tool for cleaning messy CSV and Excel files, validating records, and generating formatted Excel reports.

SheetSmith helps automate repetitive spreadsheet-cleaning tasks, including standardizing column names, handling duplicate records, validating data, and summarizing results.

## What it does

Working with messy spreadsheets often means dealing with inconsistent column names, duplicate rows, missing values, invalid emails, and incorrectly formatted dates or numbers.

SheetSmith automates common cleaning and reporting steps so the resulting data is easier to inspect and use.

## Features

- Read CSV and Excel files.
- Process supported input files from a directory.
- Normalize column names and whitespace.
- Detect and handle duplicate records.
- Handle missing values according to configured rules.
- Convert supported numeric and date fields.
- Validate configured fields such as email addresses and phone numbers.
- Apply supported data transformations.
- Export cleaned data to a formatted Excel workbook.
- Generate summary statistics and validation-error reports.
- Log processing activity and errors.
- Run from the command line.
- Include automated tests.

## Example

Input: a sales spreadsheet containing duplicate records, inconsistent column names, missing values, and invalid fields.

Run:

```bash
python -m src.main -i data/sample/sales_dirty.xlsx -o output/cleaned_sales.xlsx
```

The output workbook contains the sheets supported by the application, such as:

- `Cleaned_Data`
- `Summary`
- `Validation_Errors`
- `Processing_Log`

## Project structure

```text
sheet-smith/
├── data/
│   ├── raw/
│   └── sample/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── loader.py
│   ├── cleaner.py
│   ├── transformer.py
│   ├── validator.py
│   ├── reporter.py
│   └── logger.py
├── tests/
├── generate_sample_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.8+ (tested on Python 3.12)
- pandas>=2.0.0
- openpyxl>=3.1.0
- pytest>=7.0.0 for running tests

## Installation

Clone the repository:

```bash
git clone https://github.com/srujan2077/sheet-smith.git
cd sheet-smith
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Generate the sample dataset if required:

```bash
python generate_sample_data.py
```

Process the sample file:

```bash
python -m src.main -i data/sample/sales_dirty.xlsx -o output/cleaned_sales.xlsx
```

Process a directory of files:
```bash
python -m src.main -i data/raw/ -o output/
```

Show available CLI options:

```bash
python -m src.main --help
```

## Configuration

You can configure processing rules in `src/config.py`:
- `required_columns`: List of columns that must exist in the input data.
- `duplicate_subset`: Subset of columns used to identify duplicate records.
- `missing_value_defaults`: Dictionary mapping column names to default values for missing data.
- `email_regex` and `phone_regex`: Regular expressions used to validate email and phone number fields.
- `numeric_columns` and `date_columns`: Lists of columns that should be converted to numeric and datetime formats.

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

The test suite runs against the loader, cleaner, transformer, and validator modules.

## Limitations

- Validation rules may need to be adapted depending on the specific datasets and regions (e.g. phone numbers).
- Automated cleaning uses configured defaults for missing data; it cannot determine the correct specific value for every missing or invalid field.
- Large files may require significant memory since pandas processes data in memory.

## Possible improvements

- Support additional input formats.
- Add configurable cleaning rules.
- Expand validation and reporting options.
- Add more tests for edge cases.
