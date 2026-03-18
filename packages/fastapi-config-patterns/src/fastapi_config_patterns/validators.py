"""Reusable field validators for Pydantic settings.

Extracted from GridFlow backend/src/config.py
"""

from typing import List, Union


def assemble_cors_origins(v: Union[str, List[str]]) -> List[str]:
    """Parse CORS origins from string or list.
    
    Handles:
    - Wildcard "*" for all origins
    - Comma-separated string
    - List of strings
    
    Args:
        v: CORS origins as string or list
        
    Returns:
        List of origin strings
    
    Example:
        >>> from pydantic import field_validator
        >>> from pydantic_settings import BaseSettings
        >>> 
        >>> class Settings(BaseSettings):
        ...     allowed_origins: List[str]
        ...     
        ...     @field_validator("allowed_origins", mode="before")
        ...     @classmethod
        ...     def parse_origins(cls, v):
        ...         return assemble_cors_origins(v)
    """
    if isinstance(v, str):
        # Handle special case of "*" for all origins
        if v.strip() == "*":
            return ["*"]
        # Parse comma-separated string
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list):
        return v
    return v
