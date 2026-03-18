"""Email generation strategies for property testing.

RFC 5321 compliant email generation using property-based patterns.
RULE: Maximum 100 lines per file.
"""

from hypothesis import strategies as st


@st.composite
def email_local_part_strategy(draw, min_size=1, max_size=20):
    """Generate valid email local part (before @).
    
    Uses ASCII lowercase alphanumeric for simplicity.
    Production validators handle full RFC 5322 complexity.
    """
    return draw(st.text(
        alphabet=st.characters(
            min_codepoint=ord('a'),
            max_codepoint=ord('z')
        ) | st.characters(
            min_codepoint=ord('0'),
            max_codepoint=ord('9')
        ),
        min_size=min_size,
        max_size=max_size
    ).filter(lambda x: len(x) > 0))


@st.composite
def email_domain_part_strategy(draw, min_size=1, max_size=15):
    """Generate valid email domain (between @ and .).
    
    Uses ASCII lowercase letters only.
    """
    return draw(st.text(
        alphabet=st.characters(
            min_codepoint=ord('a'),
            max_codepoint=ord('z')
        ),
        min_size=min_size,
        max_size=max_size
    ).filter(lambda x: len(x) > 0))


@st.composite
def email_tld_strategy(draw, min_size=2, max_size=6):
    """Generate valid top-level domain.
    
    Property-based TLD generation using ASCII lowercase letters.
    Min 2 chars (per IANA), max 6 for reasonable test scope.
    """
    return draw(st.text(
        alphabet=st.characters(
            min_codepoint=ord('a'),
            max_codepoint=ord('z')
        ),
        min_size=min_size,
        max_size=max_size
    ).filter(lambda x: len(x) >= min_size))


@st.composite
def email_strategy(draw):
    """Generate valid RFC-compliant email addresses.
    
    Per RFC 5321:
    - Domain part is case-insensitive (normalized by validators)
    - Local part is technically case-sensitive (preserved by Pydantic)
    
    Returns ASCII-only lowercase emails for test consistency.
    """
    local = draw(email_local_part_strategy())
    domain = draw(email_domain_part_strategy())
    tld = draw(email_tld_strategy())
    return f"{local}@{domain}.{tld}"

