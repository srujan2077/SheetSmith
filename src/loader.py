import pandas as pd
from pathlib import Path
from src.logger import logger

def load_data(input_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV or Excel file, or a directory of files.
    """
    path = Path(input_path)
    
    if not path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        raise FileNotFoundError(f"Path not found: {input_path}")

    dfs = []
    
    if path.is_file():
        files_to_process = [path]
    else:
        files_to_process = list(path.glob('*.csv')) + list(path.glob('*.xlsx'))
        
    if not files_to_process:
        logger.error(f"No valid CSV or Excel files found in {input_path}")
        raise ValueError(f"No valid files found in {input_path}")
        
    for file in files_to_process:
        try:
            logger.info(f"Loading file: {file.name}")
            if file.suffix.lower() == '.csv':
                df = pd.read_csv(file)
            elif file.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file)
            else:
                logger.warning(f"Unsupported file format: {file.name}")
                continue
                
            dfs.append(df)
            logger.info(f"Successfully loaded {len(df)} rows from {file.name}")
            
        except Exception as e:
            logger.error(f"Error loading {file.name}: {str(e)}")
            
    if not dfs:
        raise ValueError("Could not successfully load any files.")
        
    # Combine all loaded dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total rows loaded: {len(combined_df)}")
    return combined_df
