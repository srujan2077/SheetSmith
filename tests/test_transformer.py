import pandas as pd
import pytest
from src.transformer import DataTransformer

def test_calculate_totals():
    df = pd.DataFrame({
        "quantity": [2, 3, 0, None],
        "unit_price": [10.0, 5.0, 20.0, 15.0]
    })
    transformer = DataTransformer(df)
    transformer.calculate_totals()
    
    assert "total_amount" in transformer.df.columns
    assert transformer.df["total_amount"].iloc[0] == 20.0
    assert transformer.df["total_amount"].iloc[1] == 15.0
    assert transformer.df["total_amount"].iloc[2] == 0.0
    assert pd.isna(transformer.df["total_amount"].iloc[3])
