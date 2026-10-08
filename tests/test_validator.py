import pandas as pd
import pytest
from src.validator import DataValidator

def test_email_validation():
    df = pd.DataFrame({
        "email": ["valid@example.com", "invalid-email", None]
    })
    validator = DataValidator(df)
    valid_df, invalid_df, _ = validator.validate()
    
    assert len(valid_df) == 1
    assert len(invalid_df) == 2
    assert "Invalid Email" in invalid_df["validation_errors"].iloc[0]

def test_quantity_validation():
    df = pd.DataFrame({
        "quantity": [10, -5, 0, None]
    })
    validator = DataValidator(df)
    valid_df, invalid_df, _ = validator.validate()
    
    assert len(valid_df) == 1
    assert len(invalid_df) == 3
    assert "Invalid Quantity" in invalid_df["validation_errors"].iloc[0]
