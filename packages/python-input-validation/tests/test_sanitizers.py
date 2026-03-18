"""Property-based tests for input sanitizers.

Tests email and text sanitization functions with various inputs.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_input_validation.sanitizers import (
    sanitize_email,
    sanitize_text_input,
)
from .strategies.email import email_strategy


class TestEmailSanitization:
    """Property-based tests for email sanitization."""

    @given(email=email_strategy())
    def test_sanitize_lowercases_email(self, email):
        """Sanitized email should be lowercase."""
        sanitized = sanitize_email(email)
        assert sanitized == sanitized.lower()

    @given(email=email_strategy(), whitespace=st.text(alphabet=' \t\n', max_size=5))
    def test_sanitize_strips_whitespace(self, email, whitespace):
        """Sanitized email should have whitespace removed."""
        email_with_whitespace = whitespace + email + whitespace
        sanitized = sanitize_email(email_with_whitespace)
        assert sanitized == email.lower()
        assert not sanitized.startswith(' ')
        assert not sanitized.endswith(' ')

    def test_sanitize_preserves_structure(self):
        """Sanitized email should preserve @ and domain structure."""
        email = "User@Example.COM"
        sanitized = sanitize_email(email)
        assert sanitized == "user@example.com"
        assert '@' in sanitized
        assert '.' in sanitized

    @given(email=st.emails())
    def test_sanitize_idempotent(self, email):
        """Sanitizing twice should give same result."""
        first = sanitize_email(email)
        second = sanitize_email(first)
        assert first == second

    def test_sanitize_empty_string(self):
        """Sanitizing empty string should return empty string."""
        assert sanitize_email("") == ""

    def test_sanitize_whitespace_only(self):
        """Sanitizing whitespace-only string should return empty."""
        assert sanitize_email("   ") == ""


class TestTextInputSanitization:
    """Property-based tests for text input sanitization."""

    @given(text=st.text(max_size=50), whitespace=st.text(alphabet=' \t\n', max_size=5))
    def test_sanitize_strips_whitespace(self, text, whitespace):
        """Sanitized text should have leading/trailing whitespace removed."""
        text_with_whitespace = whitespace + text + whitespace
        sanitized = sanitize_text_input(text_with_whitespace)
        assert sanitized == text.strip()

    @given(text=st.text(min_size=20, max_size=50))
    def test_sanitize_truncates_to_max_length(self, text):
        """Sanitized text should be truncated to max_length."""
        max_len = 10
        sanitized = sanitize_text_input(text, max_length=max_len)
        assert len(sanitized) <= max_len

    @given(text=st.text(max_size=10))
    def test_sanitize_preserves_short_text(self, text):
        """Text shorter than max_length should be preserved."""
        max_len = 20
        sanitized = sanitize_text_input(text, max_length=max_len)
        assert sanitized == text.strip()

    @given(text=st.text(max_size=100))
    def test_sanitize_without_max_length(self, text):
        """Sanitize without max_length should only strip."""
        sanitized = sanitize_text_input(text)
        assert sanitized == text.strip()

    @given(text=st.text(max_size=100))
    def test_sanitize_idempotent(self, text):
        """Sanitizing twice should give same result."""
        first = sanitize_text_input(text, max_length=50)
        second = sanitize_text_input(first, max_length=50)
        assert first == second

    def test_sanitize_empty_string(self):
        """Sanitizing empty string should return empty string."""
        assert sanitize_text_input("") == ""

    def test_sanitize_whitespace_only(self):
        """Sanitizing whitespace-only string should return empty."""
        assert sanitize_text_input("   \t\n   ") == ""

    def test_sanitize_exact_max_length(self):
        """Text exactly at max_length should be preserved."""
        text = "12345"
        sanitized = sanitize_text_input(text, max_length=5)
        assert sanitized == text
