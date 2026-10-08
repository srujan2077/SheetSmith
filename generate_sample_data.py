import pandas as pd
import numpy as np
from pathlib import Path
import random

def generate_dirty_data():
    np.random.seed(42)
    random.seed(42)

    # Base data
    num_rows = 50
    
    order_ids = [f"ORD-{i:04d}" for i in range(1, num_rows + 1)]
    dates = pd.date_range(start="2023-01-01", periods=num_rows, freq="D").astype(str).tolist()
    names = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Brown", "Tom Davis", "Emma Wilson", "James Jones", "Sophia Garcia"]
    domains = ["example.com", "test.org", "gmail.com"]
    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Desk"]
    categories = ["Electronics", "Accessories", "Furniture"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    payments = ["Credit Card", "PayPal", "Bank Transfer"]

    data = {
        "Order ID ": order_ids, # Extra space
        "order_date": dates,
        "CustomerName": [random.choice(names) for _ in range(num_rows)],
        " Email ": [f"{name.split()[0].lower()}@{random.choice(domains)}" for name in names] * (num_rows // len(names) + 1),
        "phone": [f"555-{random.randint(1000, 9999)}" for _ in range(num_rows)],
        "Product": [random.choice(products) for _ in range(num_rows)],
        "category ": [random.choice(categories) for _ in range(num_rows)], # Extra space
        " Quantity": [random.randint(1, 5) for _ in range(num_rows)], # Extra space
        "unit_price": [round(random.uniform(10.0, 500.0), 2) for _ in range(num_rows)],
        "city": [random.choice(cities) for _ in range(num_rows)],
        "Payment_Method": [random.choice(payments) for _ in range(num_rows)]
    }
    
    # Truncate lists to num_rows just in case
    for k in data:
        data[k] = data[k][:num_rows]

    df = pd.DataFrame(data)

    # Introduce duplicates
    df = pd.concat([df, df.iloc[[5, 12, 25]]], ignore_index=True)

    # Introduce missing values
    df.loc[3, "CustomerName"] = np.nan
    df.loc[10, " Email "] = ""
    df.loc[22, " Quantity"] = np.nan
    df.loc[45, "unit_price"] = np.nan

    # Introduce inconsistent capitalization and spaces
    df.loc[7, "CustomerName"] = " jane SMITH "
    df.loc[14, "Product"] = " laptop "
    df.loc[30, "category "] = "ELECTRONICS"
    df.loc[40, "city"] = "  chicago "

    # Introduce invalid emails
    df.loc[2, " Email "] = "invalid-email-no-domain"
    df.loc[18, " Email "] = "another@invalid@email.com"

    # Introduce invalid phone numbers
    df.loc[9, "phone"] = "invalid-phone"
    df.loc[35, "phone"] = "555-XYZ"

    # Introduce different date formats
    df.loc[1, "order_date"] = "01-02-2023" # MM-DD-YYYY or DD-MM-YYYY depending on parsing
    df.loc[20, "order_date"] = "2023/01/21"

    # Introduce incorrect numeric formatting (string instead of float/int)
    df["unit_price"] = df["unit_price"].astype(object)
    df.loc[8, "unit_price"] = "150.50"
    
    df[" Quantity"] = df[" Quantity"].astype(object)
    df.loc[27, " Quantity"] = "three"
    
    # Inconsistent category names
    df.loc[15, "category "] = "elec"
    df.loc[33, "category "] = "furn."

    # Calculate Total Amount where possible, leave some empty
    df["total_amount"] = pd.to_numeric(df[" Quantity"], errors='coerce') * pd.to_numeric(df["unit_price"], errors='coerce')
    df["total_amount"] = df["total_amount"].astype(object)
    df.loc[5, "total_amount"] = "wrong" # string type

    # Save to Excel
    output_dir = Path(__file__).parent / "data" / "sample"
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_dir / "sales_dirty.xlsx", index=False)
    print("Sample dataset 'sales_dirty.xlsx' generated successfully.")

if __name__ == "__main__":
    generate_dirty_data()
