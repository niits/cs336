import unicodedata
import regex as re


def remove_punctuation(s: str) -> str:
    """Remove punctuation from the string."""
    return re.sub(r"[^\w\s]", "", s)


def unicode_normalize_string(s: str) -> str:
    """Normalize the string to NFC form."""
    return unicodedata.normalize("NFC", s)


def remove_extra_whitespace(s: str) -> str:
    """Remove extra whitespaces from the string."""
    return re.sub(r"\s+", " ", s).strip()


def normalize_text(s: str) -> str:
    """Apply a series of normalizations to the text."""
    s = unicode_normalize_string(s)
    s = remove_extra_whitespace(s)
    return s
