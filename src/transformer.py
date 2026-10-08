import pandas as pd
from src.logger import logger

class DataTransformer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.logs = []
        
    def _log_action(self, msg: str):
        self.logs.append(msg)
        logger.info(msg)

    def calculate_totals(self):
        """
        Calculates total_amount if missing or recalculates it to be sure.
        """
        if "quantity" in self.df.columns and "unit_price" in self.df.columns:
            # Overwrite or fill total_amount
            calculated_total = self.df["quantity"] * self.df["unit_price"]
            
            if "total_amount" not in self.df.columns:
                self.df["total_amount"] = calculated_total
                self._log_action("Created 'total_amount' column.")
            else:
                # Fill missing totals
                missing_totals = self.df["total_amount"].isna()
                self.df.loc[missing_totals, "total_amount"] = calculated_total[missing_totals]
                
                # Recalculate where it doesn't match? For now just fill missing
                self._log_action(f"Calculated 'total_amount' for {missing_totals.sum()} missing rows.")
                
        return self

    def transform(self):
        self.calculate_totals()
        return self.df, self.logs
