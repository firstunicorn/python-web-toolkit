"""Generic text input strategies for property testing.

This module contains text-based Hypothesis strategies that are
truly generic and can be used for robustness testing across apps.

RULE: Maximum 100 lines per file.
"""

# Conditional import for hypothesis - only needed when running tests
try:
    from hypothesis import strategies as st
except ImportError:
    # Fallback for when hypothesis is not available
    class MockStrategies:
        @staticmethod
        def composite(func):
            def wrapper(*args, **kwargs):
                return "mock_text"
            return wrapper
        
        @staticmethod
        def text(*args, **kwargs):
            return "mock_text"
        
        @staticmethod
        def characters(*args, **kwargs):
            return "abc"
    
    st = MockStrategies()


@st.composite
def any_text_input_strategy(draw):
    """Generate any text input for robustness testing.
    
    This strategy produces any Unicode text including edge cases
    like empty strings, very long strings, and special characters.
    """
    return draw(st.text(min_size=0, max_size=200))


@st.composite
def any_non_empty_text_strategy(draw):
    """Generate any non-empty text for testing.
    
    Useful when testing functions that require non-empty string input
    but should handle any non-empty text gracefully.
    """
    return draw(st.text(min_size=1, max_size=200))


@st.composite
def safe_ascii_text_strategy(draw):
    """Generate safe ASCII text for testing.
    
    Uses printable ASCII characters (32-126) which are generally
    safe for most text processing and API interactions.
    """
    return draw(st.text(
        alphabet=st.characters(min_codepoint=32, max_codepoint=126),
        min_size=0,
        max_size=100
    ))


@st.composite
def alphanumeric_text_strategy(draw):
    """Generate alphanumeric text for testing.
    
    Contains only letters (uppercase/lowercase) and digits,
    useful for testing identifier-like inputs.
    """
    return draw(st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')),
        min_size=0,
        max_size=50
    ))


@st.composite
def whitespace_text_strategy(draw):
    """Generate text containing various whitespace characters.
    
    Useful for testing text processing functions that need to
    handle different types of whitespace correctly.
    """
    whitespace_chars = ' \t\n\r\f\v'
    return draw(st.text(
        alphabet=whitespace_chars,
        min_size=0,
        max_size=20
    ))


@st.composite
def mixed_case_text_strategy(draw):
    """Generate text with mixed uppercase and lowercase letters.
    
    Useful for testing case-sensitivity handling in text processing.
    """
    return draw(st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll')),
        min_size=0,
        max_size=50
    ))
