import pandas as pd
import re
from src.logger import logger
from src.config import config

class DataValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.valid_df = pd.DataFrame()
        self.invalid_df = pd.DataFrame()
        self.logs = []
        
    def _log_action(self, msg: str):
        self.logs.append(msg)
        logger.info(msg)

    def validate(self):
        """
        Validates the dataframe based on configured rules.
        Splits data into valid and invalid dataframes.
        """
        # Create an error column
        errors = pd.Series([""] * len(self.df), index=self.df.index)
        
        # 1. Email validation
        if "email" in self.df.columns:
            email_pattern = re.compile(config.email_regex)
            invalid_emails = self.df["email"].apply(lambda x: pd.isna(x) or not bool(email_pattern.match(str(x))))
            errors[invalid_emails] += "Invalid Email; "
            
        # 2. Phone validation (optional column)
        if "phone" in self.df.columns:
            phone_pattern = re.compile(config.phone_regex)
            # empty string or nan is considered missing, but maybe we only flag if it's there and invalid
            invalid_phones = self.df["phone"].apply(
                lambda x: pd.notna(x) and x != "" and str(x) != "nan" and not bool(phone_pattern.match(str(x)))
            )
            errors[invalid_phones] += "Invalid Phone; "

        # 3. Numeric constraints (e.g. quantity > 0, price >= 0)
        if "quantity" in self.df.columns:
            invalid_qty = self.df["quantity"].apply(lambda x: pd.isna(x) or x <= 0)
            errors[invalid_qty] += "Invalid Quantity; "
            
        if "unit_price" in self.df.columns:
            invalid_price = self.df["unit_price"].apply(lambda x: pd.isna(x) or x < 0)
            errors[invalid_price] += "Invalid Unit Price; "

        # 4. Date validation
        if "order_date" in self.df.columns:
            invalid_dates = self.df["order_date"].isna()
            errors[invalid_dates] += "Invalid/Missing Date; "

        # Split data
        self.df["validation_errors"] = errors.str.strip()
        
        self.valid_df = self.df[self.df["validation_errors"] == ""].drop(columns=["validation_errors"])
        self.invalid_df = self.df[self.df["validation_errors"] != ""]
        
        self._log_action(f"Validation complete. Valid records: {len(self.valid_df)}, Invalid records: {len(self.invalid_df)}")
        
        return self.valid_df, self.invalid_df, self.logs
