"""Configuration management for the application."""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class AppConfig(BaseModel):
    """Application configuration."""
    
    openai_api_key: str = Field(..., description="OpenAI API key")
    excel_file_path: str = Field(default="data/input.xlsx", description="Path to Excel file")
    email_prompt_template: str = Field(
        default="Generate a personalized and professional email based on the following data: {data}",
        description="Template for email generation prompt"
    )
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True


def load_config() -> AppConfig:
    """Load configuration from environment variables.
    
    Returns:
        AppConfig: Application configuration object
        
    Raises:
        ValueError: If required configuration is missing
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )
    
    return AppConfig(
        openai_api_key=openai_api_key,
        excel_file_path=os.getenv("EXCEL_FILE_PATH", "data/input.xlsx"),
        email_prompt_template=os.getenv(
            "EMAIL_PROMPT_TEMPLATE",
            "Generate a personalized and professional email based on the following data: {data}"
        ),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    )
