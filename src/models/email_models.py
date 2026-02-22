"""Data models for the email generator application."""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class RowData(BaseModel):
    """Model representing a single row from the Excel sheet."""
    
    row_number: int = Field(..., description="The row number in the Excel sheet")
    data: Dict[str, Any] = Field(..., description="Dictionary of column names to values")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert row data to dictionary format."""
        return self.data
    
    def __str__(self) -> str:
        """String representation of row data."""
        return f"Row {self.row_number}: {self.data}"


class GeneratedEmail(BaseModel):
    """Model representing a generated email."""
    
    row_number: int = Field(..., description="The row number this email was generated for")
    email_content: str = Field(..., description="The generated email content")
    row_data: Dict[str, Any] = Field(..., description="The original row data")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    
    @property
    def is_success(self) -> bool:
        """Check if email generation was successful."""
        return self.error is None
    
    def __str__(self) -> str:
        """String representation of generated email."""
        if self.is_success:
            return f"Email for Row {self.row_number}:\n{self.email_content}"
        return f"Failed to generate email for Row {self.row_number}: {self.error}"
