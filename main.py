"""Peter Atef"""
"""Main entry point for the Excel to Email generator application."""
import logging
import sys
from pathlib import Path

from src.config import load_config
from src.controllers import EmailGeneratorController


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('email_generator.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the email generation workflow."""
    try:
        logger.info("=" * 80)
        logger.info("Starting Excel to Email Generator Application")
        logger.info("=" * 80)
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        logger.info(f"Configuration loaded. Excel file: {config.excel_file_path}")
        
        # Initialize controller
        logger.info("Initializing email generator controller...")
        controller = EmailGeneratorController(config)
        
        # Process all rows and generate emails
        logger.info("Processing Excel rows and generating emails...")
        generated_emails = controller.process_all_rows()
        
        # Save emails to file
        logger.info("Saving generated emails to file...")
        controller.save_emails_to_file(generated_emails)
        
        # Print summary
        successful = sum(1 for e in generated_emails if e.is_success)
        failed = len(generated_emails) - successful
        
        print("\n" + "=" * 80)
        print("EMAIL GENERATION SUMMARY")
        print("=" * 80)
        print(f"Total rows processed: {len(generated_emails)}")
        print(f"Successfully generated: {successful}")
        print(f"Failed: {failed}")
        print(f"Output saved to: output/generated_emails.txt")
        print("=" * 80 + "\n")
        
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application failed with error: {str(e)}", exc_info=True)
        print(f"\nERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
