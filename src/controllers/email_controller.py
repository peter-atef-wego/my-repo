"""Controller layer for orchestrating the email generation workflow."""
import logging
from typing import List
from pathlib import Path

from ..config import AppConfig
from ..data import ExcelReader
from ..services import EmailGenerationService
from ..models import RowData, GeneratedEmail


logger = logging.getLogger(__name__)


class EmailGeneratorController:
    """Controller that orchestrates reading Excel data and generating emails."""
    
    def __init__(self, config: AppConfig):
        """Initialize the controller.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.excel_reader = ExcelReader(config.excel_file_path)
        self.email_service = EmailGenerationService(config)
        logger.info("EmailGeneratorController initialized")
    
    def process_all_rows(self) -> List[GeneratedEmail]:
        """Process all rows from the Excel file and generate emails.
        
        Returns:
            List of GeneratedEmail objects
        """
        logger.info("Starting to process all rows")
        
        # Read all rows from Excel
        rows = self.excel_reader.read_all_rows()
        total_rows = len(rows)
        
        if total_rows == 0:
            logger.warning("No rows to process")
            return []
        
        logger.info(f"Processing {total_rows} rows")
        
        # Generate emails for each row
        generated_emails = []
        for idx, row in enumerate(rows, 1):
            logger.info(f"Processing row {idx}/{total_rows}")
            
            email = self.email_service.generate_email(
                row_number=row.row_number,
                row_data=row.data
            )
            
            generated_emails.append(email)
            
            if email.is_success:
                logger.info(f"Successfully generated email for row {row.row_number}")
            else:
                logger.error(f"Failed to generate email for row {row.row_number}: {email.error}")
        
        # Log summary
        successful = sum(1 for e in generated_emails if e.is_success)
        failed = total_rows - successful
        logger.info(f"Processing complete. Success: {successful}, Failed: {failed}")
        
        return generated_emails
    
    def process_rows_streaming(self):
        """Process rows one at a time using a generator (memory efficient).
        
        Yields:
            GeneratedEmail objects one at a time
        """
        logger.info("Starting to process rows with streaming")
        
        row_count = self.excel_reader.get_row_count()
        logger.info(f"Total rows to process: {row_count}")
        
        processed = 0
        for row in self.excel_reader.read_rows_generator():
            processed += 1
            logger.info(f"Processing row {processed}/{row_count}")
            
            email = self.email_service.generate_email(
                row_number=row.row_number,
                row_data=row.data
            )
            
            if email.is_success:
                logger.info(f"Successfully generated email for row {row.row_number}")
            else:
                logger.error(f"Failed to generate email for row {row.row_number}: {email.error}")
            
            yield email
        
        logger.info(f"Streaming processing complete. Total processed: {processed}")
    
    def save_emails_to_file(self, emails: List[GeneratedEmail], output_path: str = "output/generated_emails.txt"):
        """Save generated emails to a text file.
        
        Args:
            emails: List of generated emails
            output_path: Path where to save the output file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for email in emails:
                f.write("=" * 80 + "\n")
                f.write(f"ROW NUMBER: {email.row_number}\n")
                f.write("-" * 80 + "\n")
                
                if email.is_success:
                    f.write(f"{email.email_content}\n")
                else:
                    f.write(f"ERROR: {email.error}\n")
                
                f.write("\n" + "=" * 80 + "\n\n")
        
        logger.info(f"Saved {len(emails)} emails to {output_path}")
