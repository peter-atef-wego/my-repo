"""
Example usage of the Email Generator application.

This file demonstrates different ways to use the application components.
"""

import sys
sys.path.insert(0, '.')

from src.config import load_config, AppConfig
from src.data import ExcelReader
from src.services import EmailGenerationService
from src.controllers import EmailGeneratorController
from src.models import RowData, GeneratedEmail


def example_1_basic_usage():
    """Example 1: Basic usage with the controller (recommended approach)."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage with Controller")
    print("=" * 70)
    
    # This is the recommended way to use the application
    # The controller handles all the complexity
    
    try:
        # Load configuration from environment
        config = load_config()
        
        # Initialize controller
        controller = EmailGeneratorController(config)
        
        # Process all rows and generate emails
        emails = controller.process_all_rows()
        
        # Save to file
        controller.save_emails_to_file(emails)
        
        print(f"✓ Generated {len(emails)} emails")
        print(f"✓ Saved to output/generated_emails.txt")
        
    except ValueError as e:
        print(f"⚠ Configuration error: {e}")
        print("  Make sure to set OPENAI_API_KEY in your .env file")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_2_streaming():
    """Example 2: Memory-efficient streaming for large files."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Streaming Processing (for large files)")
    print("=" * 70)
    
    try:
        config = load_config()
        controller = EmailGeneratorController(config)
        
        # Process rows one at a time (memory efficient)
        for email in controller.process_rows_streaming():
            if email.is_success:
                print(f"✓ Generated email for row {email.row_number}")
            else:
                print(f"✗ Failed for row {email.row_number}: {email.error}")
                
    except ValueError as e:
        print(f"⚠ Configuration error: {e}")
        print("  Make sure to set OPENAI_API_KEY in your .env file")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_custom_usage():
    """Example 3: Custom usage with individual components."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Custom Usage with Individual Components")
    print("=" * 70)
    
    # You can also use individual components for more control
    
    # Step 1: Read Excel data
    print("\n1. Reading Excel data...")
    reader = ExcelReader('data/input.xlsx')
    rows = reader.read_all_rows()
    print(f"   ✓ Read {len(rows)} rows")
    
    # Step 2: Display the data (without calling OpenAI)
    print("\n2. Data from Excel:")
    for row in rows:
        print(f"   Row {row.row_number}:")
        for key, value in row.data.items():
            print(f"     {key}: {value}")
        print()
    
    # Step 3: Generate emails (requires API key)
    # Uncomment below to actually generate emails
    """
    try:
        config = load_config()
        email_service = EmailGenerationService(config)
        
        for row in rows:
            email = email_service.generate_email(row.row_number, row.data)
            if email.is_success:
                print(f"Generated email for row {row.row_number}")
                print(email.email_content[:100] + "...")
    except ValueError as e:
        print(f"Cannot generate emails: {e}")
    """


def example_4_custom_config():
    """Example 4: Using custom configuration."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Custom Configuration")
    print("=" * 70)
    
    # You can create custom configuration programmatically
    custom_config = AppConfig(
        openai_api_key="your-api-key",  # Replace with actual key
        excel_file_path="data/input.xlsx",
        email_prompt_template="Write a professional email for: {data}",
        openai_model="gpt-4"  # Use GPT-4 instead of default
    )
    
    print(f"✓ Custom config created")
    print(f"  - Excel file: {custom_config.excel_file_path}")
    print(f"  - Model: {custom_config.openai_model}")
    print(f"  - Template: {custom_config.email_prompt_template[:50]}...")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("EMAIL GENERATOR - USAGE EXAMPLES")
    print("=" * 70)
    
    # Example 3 doesn't require OpenAI API, so it always works
    example_3_custom_usage()
    
    # Example 4 shows configuration
    example_4_custom_config()
    
    # Examples 1 and 2 require OpenAI API key
    print("\n" + "=" * 70)
    print("NOTE: Examples 1 and 2 require OPENAI_API_KEY to be set")
    print("=" * 70)
    print("\nTo run examples that use OpenAI:")
    print("1. Copy .env.example to .env")
    print("2. Add your OpenAI API key to .env")
    print("3. Run: python main.py")
    print("\nOr uncomment the examples below and run this script again:")
    print("  - example_1_basic_usage()")
    print("  - example_2_streaming()")
    
    # Uncomment these to run when you have API key set up:
    # example_1_basic_usage()
    # example_2_streaming()


if __name__ == "__main__":
    main()
