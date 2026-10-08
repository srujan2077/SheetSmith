# DataCleanerPro

DataCleanerPro is a production-quality Python automation tool designed to streamline the processing, cleaning, and reporting of dirty data in CSV or Excel formats.

It takes raw, unformatted, and error-prone datasets and automatically normalizes, validates, and transforms them into a professional Excel report. This tool is perfect for data engineers, analysts, or anyone who frequently receives messy data from clients and needs a standardized way to clean it.

## Problem Being Solved

In real-world scenarios, data received from clients or third-party systems is rarely clean. It often contains:
- Inconsistent column naming
- Duplicate records
- Missing values in critical fields
- Invalid data types (e.g., text in numeric fields)
- Malformed data (e.g., invalid emails or phone numbers)

Cleaning this manually in Excel is time-consuming and error-prone. DataCleanerPro automates this entire pipeline.

## Features

- **Multi-format Ingestion**: Processes single files or entire directories of `.csv` and `.xlsx` files.
- **Auto-Normalization**: Strips whitespace, standardizes capitalization, and formats column names (e.g., ` Order ID ` -> `order_id`).
- **Deduplication**: Intelligently removes duplicate records based on configurable keys.
- **Missing Value Handling**: Fills missing values with sensible defaults (e.g., `0` for numeric, `Unknown` for text).
- **Data Type Conversion**: Ensures numeric columns are actually numbers and standardizes date formats.
- **Validation Rules**: Uses Regular Expressions to validate emails and phone numbers, segregating invalid rows.
- **Transformation**: Performs basic business logic calculations (e.g., `quantity * unit_price = total_amount`).
- **Comprehensive Reporting**: Generates a multi-sheet Excel workbook containing:
  - `Cleaned_Data`: The final, analysis-ready dataset.
  - `Summary`: High-level statistics (Total records, Sales, etc.).
  - `Validation_Errors`: Rows that failed validation, with reasons.
  - `Processing_Log`: Detailed step-by-step logs of what the tool did.

## Architecture

The project is built using a clean, modular, and extensible architecture:

```
project/
│
├── src/                    # Source code
│   ├── main.py             # CLI Entry point
│   ├── config.py           # Centralized configuration (rules, defaults)
│   ├── loader.py           # Robust file ingestion
│   ├── cleaner.py          # Data normalization and cleaning logic
│   ├── transformer.py      # Business logic and calculations
│   ├── validator.py        # Data validation and error segregation
│   └── reporter.py         # Multi-sheet Excel report generation
│
├── data/
│   └── sample/             # Contains 'sales_dirty.xlsx' for demonstration
│
├── output/                 # Destination for processed reports
│
├── tests/                  # Pytest suite
│
├── requirements.txt        # Python dependencies
└── README.md
```

## Technologies Used

- **Python 3.8+**
- **pandas**: Core data manipulation.
- **openpyxl**: Excel file reading/writing.
- **pytest**: Unit testing.
- **argparse**: Command-line interface.
- **logging**: Professional logging mechanism.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/DataCleanerPro.git
   cd DataCleanerPro
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface (CLI)

DataCleanerPro is executed via the command line.

**Process a single file:**
```bash
python -m src.main --input data/sample/sales_dirty.xlsx --output output/cleaned_sales.xlsx
```

**Process a directory of files:**
```bash
python -m src.main --input data/raw/ --output output/
```

### Configuration

You can easily modify the processing rules by editing `src/config.py`.
- `required_columns`: List of columns that must exist.
- `duplicate_subset`: Columns used to identify duplicates.
- `missing_value_defaults`: Dictionary mapping columns to their default fill values.
- `email_regex` / `phone_regex`: Regex patterns for validation.
- `numeric_columns` / `date_columns`: Lists defining data types.

## Example Workflow

1. A client provides a messy spreadsheet: `sales_dirty.xlsx`.
2. You run: `python -m src.main -i data/sample/sales_dirty.xlsx -o output/report.xlsx`.
3. The tool logs its progress to the console and to `output/logs/`.
4. You open `output/report.xlsx` and find:
   - Clean data ready for Tableau/PowerBI.
   - A summary sheet showing total sales and records processed.
   - A validation errors sheet showing the 5 records with invalid emails that need manual review.

## Testing

To run the automated test suite:

```bash
python -m pytest tests/
```

## Future Improvements

- Add support for database connections (SQL ingestion/export).
- Implement a graphical user interface (GUI) or web dashboard.
- Add advanced outlier detection using statistical methods.

## License

MIT License
