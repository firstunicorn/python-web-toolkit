"""Property-based tests for filename operations.

Tests filename sanitization and extension extraction.
RULE: Maximum 100 lines per file.
"""

import pytest
from hypothesis import given, strategies as st

from python_technical_primitives.text.operations import (
    sanitize_filename,
    extract_extension,
)
from ..strategies.text import safe_ascii_text_strategy


class TestFilenameSanitization:
    """Property-based tests for filename sanitization."""

    @given(filename=safe_ascii_text_strategy())
    def test_sanitize_removes_invalid_chars(self, filename):
        """Sanitized filename should not contain invalid characters."""
        result = sanitize_filename(filename)
        invalid_chars = '<>:"/\\|?*'
        assert not any(c in result for c in invalid_chars)

    @given(filename=st.text(min_size=1, max_size=50))
    def test_sanitize_never_returns_empty(self, filename):
        """sanitize_filename should never return empty string."""
        result = sanitize_filename(filename)
        assert len(result) > 0

    def test_sanitize_handles_empty_string(self):
        """Empty string should return 'unnamed'."""
        assert sanitize_filename("") == "unnamed"

    def test_sanitize_replaces_spaces_with_underscores(self):
        """Spaces should be replaced with underscores."""
        result = sanitize_filename("my file name.txt")
        assert " " not in result
        assert "_" in result

    def test_sanitize_removes_leading_trailing_dots(self):
        """Leading/trailing dots should be removed."""
        result = sanitize_filename("...file...")
        assert not result.startswith(".")
        assert not result.endswith(".")

    @given(filename=safe_ascii_text_strategy())
    def test_sanitize_is_idempotent(self, filename):
        """Sanitizing twice should give same result."""
        first = sanitize_filename(filename)
        second = sanitize_filename(first)
        assert first == second


class TestExtensionExtraction:
    """Tests for file extension extraction."""

    def test_extract_extension_basic(self):
        """Extract extension from basic filename."""
        assert extract_extension("file.txt") == "txt"
        assert extract_extension("image.PNG") == "png"

    def test_extract_extension_no_extension(self):
        """Filename without extension should return None."""
        assert extract_extension("readme") is None

    def test_extract_extension_multiple_dots(self):
        """Filename with multiple dots should extract last extension."""
        assert extract_extension("archive.tar.gz") == "gz"
        assert extract_extension("my.file.name.doc") == "doc"

    @given(ext=st.text(alphabet=st.characters(whitelist_categories=('Ll',)), min_size=2, max_size=4))
    def test_extract_extension_lowercases(self, ext):
        """Extracted extension should be lowercase."""
        filename = f"file.{ext.upper()}"
        result = extract_extension(filename)
        if result:
            assert result == result.lower()

    def test_extract_extension_empty_after_dot(self):
        """Filename ending with dot should return empty extension."""
        result = extract_extension("file.")
        assert result == ""

    @given(
        filename=st.text(alphabet=st.characters(blacklist_characters='./\\'), min_size=1, max_size=20),
        ext=st.text(alphabet=st.characters(whitelist_categories=('Ll', 'Nd')), min_size=2, max_size=4)
    )
    def test_extract_extension_property(self, filename, ext):
        """Extension extraction should be consistent for valid filenames."""
        # Only test with extensions that don't contain dots or slashes
        if '.' not in ext and '/' not in ext and '\\' not in ext:
            full_name = f"{filename}.{ext}"
            result = extract_extension(full_name)
            assert result == ext.lower()
