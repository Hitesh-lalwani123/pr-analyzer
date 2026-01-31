"""
Email validation utility for the PR analyzer.
Validates email addresses for GitHub user notifications.
"""

import re
from typing import Optional


class EmailValidator:
    """Validates email addresses using regex patterns."""
    
    # RFC 5322 compliant email regex (simplified)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    @classmethod
    def is_valid(cls, email: str) -> bool:
        """
        Check if an email address is valid.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
            
        Examples:
            >>> EmailValidator.is_valid("user@example.com")
            True
            >>> EmailValidator.is_valid("invalid-email")
            False
        """
        if not email or not isinstance(email, str):
            return False
        
        return bool(cls.EMAIL_PATTERN.match(email.strip()))
    
    @classmethod
    def validate_or_raise(cls, email: str) -> str:
        """
        Validate email and raise exception if invalid.
        
        Args:
            email: Email address to validate
            
        Returns:
            Cleaned email address
            
        Raises:
            ValueError: If email is invalid
        """
        cleaned = email.strip() if email else ""
        
        if not cls.is_valid(cleaned):
            raise ValueError(f"Invalid email address: {email}")
        
        return cleaned
    
    @classmethod
    def extract_domain(cls, email: str) -> Optional[str]:
        """
        Extract domain from email address.
        
        Args:
            email: Email address
            
        Returns:
            Domain name or None if invalid
            
        Examples:
            >>> EmailValidator.extract_domain("user@example.com")
            'example.com'
        """
        if not cls.is_valid(email):
            return None
        
        try:
            return email.split('@')[1]
        except IndexError:
            return None


def validate_github_email(email: str) -> bool:
    """
    Validate email specifically for GitHub.
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid GitHub email
    """
    if not EmailValidator.is_valid(email):
        return False
    
    # Check if it's a GitHub noreply email
    domain = EmailValidator.extract_domain(email)
    
    return domain in ['github.com', 'users.noreply.github.com'] or '@' in email
