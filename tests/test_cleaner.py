import pandas as pd
import pytest
from src.cleaner import DataCleaner

def test_normalize_columns():
    df = pd.DataFrame({" Order ID ": [1, 2], "CustomerName": ["A", "B"]})
    cleaner = DataCleaner(df)
    cleaner.normalize_columns()
    assert list(cleaner.df.columns) == ["order_id", "customername"]

def test_remove_duplicates():
    df = pd.DataFrame({
        "order_id": [1, 1, 2], 
        "val": ["A", "A", "B"]
    })
    cleaner = DataCleaner(df)
    cleaner.remove_duplicates()
    assert len(cleaner.df) == 2

def test_fill_missing_values():
    df = pd.DataFrame({"quantity": [1, None, 3]})
    cleaner = DataCleaner(df)
    cleaner.fill_missing_values()
    assert cleaner.df["quantity"].iloc[1] == 0

def test_normalize_strings():
    df = pd.DataFrame({
        "customername": [" john doe ", "JANE SMITH"],
        "email": ["JOHN@TEST.COM", " jane@test.com "]
    })
    cleaner = DataCleaner(df)
    cleaner.normalize_strings()
    
    assert cleaner.df["customername"].iloc[0] == "John Doe"
    assert cleaner.df["customername"].iloc[1] == "Jane Smith"
    assert cleaner.df["email"].iloc[0] == "john@test.com"
    assert cleaner.df["email"].iloc[1] == "jane@test.com"
