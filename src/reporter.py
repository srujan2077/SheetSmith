import pandas as pd
from pathlib import Path
from src.logger import logger

def generate_report(valid_df: pd.DataFrame, invalid_df: pd.DataFrame, all_logs: list, output_path: str):
    """
    Generates the final Excel report with multiple sheets.
    """
    try:
        path = Path(output_path)
        
        if path.is_dir():
            path = path / "cleaned_data_report.xlsx"
            
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create summary data
        summary_data = {
            "Metric": [
                "Total Records Processed",
                "Valid Records",
                "Invalid Records",
                "Total Sales Amount",
                "Average Order Value",
                "Total Quantity Sold"
            ],
            "Value": [
                len(valid_df) + len(invalid_df),
                len(valid_df),
                len(invalid_df),
                valid_df["total_amount"].sum() if "total_amount" in valid_df else 0,
                valid_df["total_amount"].mean() if "total_amount" in valid_df else 0,
                valid_df["quantity"].sum() if "quantity" in valid_df else 0
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        
        # Logs dataframe
        logs_df = pd.DataFrame({"Processing_Log": all_logs})
        
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            valid_df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            invalid_df.to_excel(writer, sheet_name="Validation_Errors", index=False)
            logs_df.to_excel(writer, sheet_name="Processing_Log", index=False)
            
            # Auto-adjust column widths
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column_cells in worksheet.columns:
                    max_length = 0
                    column = column_cells[0].column_letter
                    for cell in column_cells:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column].width = adjusted_width
            
        logger.info(f"Successfully generated report at {path}")
        return str(path)
        
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        raise
