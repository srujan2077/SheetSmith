import argparse
import sys
from pathlib import Path

from src.logger import logger
from src.loader import load_data
from src.cleaner import DataCleaner
from src.transformer import DataTransformer
from src.validator import DataValidator
from src.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(
        description="DataCleanerPro: A professional Python Excel/CSV Data Cleaning & Reporting Automation Tool."
    )
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to input file or directory containing CSV/Excel files."
    )
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Path to output file or directory where the report will be saved."
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("=== Data Processing Started ===")
        all_logs = []
        
        # 1. Load Data
        df = load_data(args.input)
        all_logs.append(f"Loaded {len(df)} rows from {args.input}")
        
        # 2. Clean Data
        logger.info("Starting data cleaning...")
        cleaner = DataCleaner(df)
        cleaned_df, clean_logs = cleaner.clean()
        all_logs.extend(clean_logs)
        
        # 3. Transform Data
        logger.info("Starting data transformation...")
        transformer = DataTransformer(cleaned_df)
        transformed_df, transform_logs = transformer.transform()
        all_logs.extend(transform_logs)
        
        # 4. Validate Data
        logger.info("Starting data validation...")
        validator = DataValidator(transformed_df)
        valid_df, invalid_df, valid_logs = validator.validate()
        all_logs.extend(valid_logs)
        
        # 5. Generate Report
        logger.info("Generating report...")
        report_path = generate_report(valid_df, invalid_df, all_logs, args.output)
        
        logger.info(f"=== Data Processing Completed successfully. Output saved to {report_path} ===")
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
