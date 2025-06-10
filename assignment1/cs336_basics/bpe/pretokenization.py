from typing import Iterable
import regex as re


PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

COMPILED_PATTERN = re.compile(PAT, flags=re.V0 | re.UNICODE)


def split_text_into_iterator(text: str) -> Iterable[re.Match]:
    return COMPILED_PATTERN.finditer(text)
