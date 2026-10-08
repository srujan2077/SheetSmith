from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class CleanerConfig:
    # Columns that must be present in the input file
    required_columns: List[str] = field(default_factory=lambda: [
        "order_id", "order_date", "customername", "email", 
        "product", "category", "quantity", "unit_price", "total_amount"
    ])
    
    # Columns to check for duplicates (if empty, checks all columns)
    duplicate_subset: List[str] = field(default_factory=lambda: ["order_id"])
    
    # How to handle missing values (column_name: default_value)
    missing_value_defaults: Dict[str, str] = field(default_factory=lambda: {
        "quantity": 0,
        "unit_price": 0.0,
        "category": "Unknown",
        "city": "Unknown"
    })
    
    # Validation rules
    email_regex: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    phone_regex: str = r"^\+?[0-9\-\s\(\)]+$"
    
    # Column types for conversion
    numeric_columns: List[str] = field(default_factory=lambda: ["quantity", "unit_price", "total_amount"])
    date_columns: List[str] = field(default_factory=lambda: ["order_date"])

config = CleanerConfig()
