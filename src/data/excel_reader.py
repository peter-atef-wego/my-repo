"""Data layer for reading Excel files."""
import logging
from typing import List, Generator
import pandas as pd
from pathlib import Path

from ..models import RowData


logger = logging.getLogger(__name__)


class ExcelReader:
    """Reader for Excel files that provides row-by-row data access."""
    
    def __init__(self, file_path: str):
        """Initialize Excel reader.
        
        Args:
            file_path: Path to the Excel file
            
        Raises:
            FileNotFoundError: If the Excel file doesn't exist
            ValueError: If the file is not a valid Excel file
        """
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        if self.file_path.suffix not in ['.xlsx', '.xls']:
            raise ValueError(f"Invalid file type: {self.file_path.suffix}. Expected .xlsx or .xls")
        
        logger.info(f"Initialized ExcelReader for file: {file_path}")
    
    def read_all_rows(self) -> List[RowData]:
        """Read all rows from the Excel file.
        
        Returns:
            List of RowData objects containing the data from each row
            
        Raises:
            Exception: If there's an error reading the Excel file
        """
        try:
            logger.info(f"Reading Excel file: {self.file_path}")
            df = pd.read_excel(self.file_path)
            
            if df.empty:
                logger.warning("Excel file is empty")
                return []
            
            rows = []
            for idx, row in df.iterrows():
                row_data = RowData(
                    row_number=idx + 2,  # +2 because Excel is 1-indexed and has header row
                    data=row.to_dict()
                )
                rows.append(row_data)
            
            logger.info(f"Successfully read {len(rows)} rows from Excel file")
            return rows
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise
    
    def read_rows_generator(self) -> Generator[RowData, None, None]:
        """Read rows from Excel file as a generator for memory efficiency.
        
        Yields:
            RowData objects one at a time
            
        Raises:
            Exception: If there's an error reading the Excel file
        """
        try:
            logger.info(f"Reading Excel file with generator: {self.file_path}")
            df = pd.read_excel(self.file_path)
            
            if df.empty:
                logger.warning("Excel file is empty")
                return
            
            for idx, row in df.iterrows():
                row_data = RowData(
                    row_number=idx + 2,  # +2 because Excel is 1-indexed and has header row
                    data=row.to_dict()
                )
                yield row_data
                
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise
    
    def get_row_count(self) -> int:
        """Get the total number of data rows in the Excel file.
        
        Returns:
            Number of rows (excluding header)
        """
        try:
            df = pd.read_excel(self.file_path)
            return len(df)
        except Exception as e:
            logger.error(f"Error counting rows: {str(e)}")
            raise
