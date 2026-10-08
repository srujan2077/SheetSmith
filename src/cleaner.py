import pandas as pd
import numpy as np
from src.logger import logger
from src.config import config

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.logs = []
        
    def _log_action(self, msg: str):
        self.logs.append(msg)
        logger.info(msg)

    def normalize_columns(self):
        """Lowercase and remove leading/trailing spaces from column names, replace spaces with underscores."""
        original_cols = self.df.columns.tolist()
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(r'\s+', '_', regex=True)
        )
        self._log_action(f"Normalized column names. Original: {original_cols}, New: {self.df.columns.tolist()}")
        return self

    def check_required_columns(self):
        """Ensure all required columns exist."""
        missing = [col for col in config.required_columns if col not in self.df.columns]
        if missing:
            logger.error(f"Missing required columns: {missing}")
            raise ValueError(f"Missing required columns: {missing}")
        return self

    def remove_duplicates(self):
        """Remove duplicate rows based on subset configuration."""
        initial_count = len(self.df)
        subset = [c for c in config.duplicate_subset if c in self.df.columns]
        
        if subset:
            self.df.drop_duplicates(subset=subset, inplace=True, keep='first')
        else:
            self.df.drop_duplicates(inplace=True, keep='first')
            
        final_count = len(self.df)
        removed = initial_count - final_count
        self._log_action(f"Removed {removed} duplicate rows.")
        return self

    def fill_missing_values(self):
        """Fill missing values based on defaults."""
        for col, default_val in config.missing_value_defaults.items():
            if col in self.df.columns:
                missing_count = self.df[col].isna().sum()
                if missing_count > 0:
                    self.df[col] = self.df[col].fillna(default_val)
                    self._log_action(f"Filled {missing_count} missing values in '{col}' with '{default_val}'")
        return self

    def normalize_strings(self):
        """Strip whitespace and fix capitalization for string columns."""
        for col in self.df.select_dtypes(include=['object', 'string']):
            # Strip whitespace
            self.df[col] = self.df[col].apply(lambda x: str(x).strip() if pd.notna(x) else x)
            
            # Simple title case for likely name/category columns, lower for emails
            if "name" in col or "category" in col or "city" in col:
                self.df[col] = self.df[col].apply(lambda x: str(x).title() if pd.notna(x) else x)
            elif "email" in col:
                self.df[col] = self.df[col].apply(lambda x: str(x).lower() if pd.notna(x) else x)
        
        self._log_action("Normalized string formatting (whitespace, capitalization).")
        return self

    def convert_data_types(self):
        """Convert numeric and date columns to proper types."""
        # Numeric conversions
        for col in config.numeric_columns:
            if col in self.df.columns:
                # Coerce errors to NaN, which can be caught by validation or handled
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Date conversions
        for col in config.date_columns:
            if col in self.df.columns:
                # Convert to datetime, then to consistent string format or keep as datetime
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce').dt.date
                
        self._log_action(f"Converted data types for numeric {config.numeric_columns} and dates {config.date_columns}")
        return self

    def clean(self) -> pd.DataFrame:
        """Run all cleaning steps and return cleaned dataframe."""
        self.normalize_columns()
        self.check_required_columns()
        self.remove_duplicates()
        self.fill_missing_values()
        self.normalize_strings()
        self.convert_data_types()
        
        return self.df, self.logs
