"""Service layer for OpenAI email generation."""
import logging
import json
from typing import Dict, Any
from openai import OpenAI

from ..models import GeneratedEmail
from ..config import AppConfig


logger = logging.getLogger(__name__)


class EmailGenerationService:
    """Service for generating personalized emails using OpenAI."""
    
    def __init__(self, config: AppConfig):
        """Initialize the email generation service.
        
        Args:
            config: Application configuration containing OpenAI settings
        """
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        logger.info(f"Initialized EmailGenerationService with model: {config.openai_model}")
    
    def generate_email(self, row_number: int, row_data: Dict[str, Any]) -> GeneratedEmail:
        """Generate a personalized email based on row data.
        
        Args:
            row_number: The row number from the Excel sheet
            row_data: Dictionary containing the row data
            
        Returns:
            GeneratedEmail object containing the generated email or error
        """
        try:
            logger.info(f"Generating email for row {row_number}")
            
            # Format the data for the prompt
            data_str = json.dumps(row_data, indent=2)
            prompt = self.config.email_prompt_template.format(data=data_str)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional email writer. Generate personalized, well-structured emails based on the provided data."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            email_content = response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated email for row {row_number}")
            
            return GeneratedEmail(
                row_number=row_number,
                email_content=email_content,
                row_data=row_data
            )
            
        except Exception as e:
            logger.error(f"Error generating email for row {row_number}: {str(e)}")
            return GeneratedEmail(
                row_number=row_number,
                email_content="",
                row_data=row_data,
                error=str(e)
            )
    
    def test_connection(self) -> bool:
        """Test the OpenAI API connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Make a simple API call to test the connection
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            logger.info("OpenAI API connection test successful")
            return True
        except Exception as e:
            logger.error(f"OpenAI API connection test failed: {str(e)}")
            return False
