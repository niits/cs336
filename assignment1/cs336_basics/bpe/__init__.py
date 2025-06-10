from cs336_basics.bpe.utils import find_chunk_boundaries
from cs336_basics.bpe.normalization import normalize_text
import os
import logging
import multiprocessing
from typing import DefaultDict
from cs336_basics.bpe.tokenization import count_word_frequencies, get_alphabet
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict
from cs336_basics.bpe.tokenization import split_words
from cs336_basics.bpe.tokenization import train_bpe_tokenizer

logger = logging.getLogger(__name__)


def split_text_into_chunks(
    input_path: str | os.PathLike,
    chunk_start: int,
    chunk_end: int,
) -> DefaultDict[bytes, int]:
    """
    Splits the text file into chunks of specified size.
    Returns a list of tuples with start and end byte positions for each chunk.
    """
    with open(input_path, "rb") as f:

        f.seek(chunk_start)
        chunk = f.read(chunk_end - chunk_start)

    chunk_str = chunk.decode("utf-8", errors="ignore")

    normalized_chunk = normalize_text(chunk_str)

    return count_word_frequencies(normalized_chunk)


def train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str],
):

    num_cores = multiprocessing.cpu_count()

    with open(input_path, "rb") as f:
        boundaries = find_chunk_boundaries(
            f, num_cores, "<|endoftext|>".encode("utf-8")
        )
        logger.info("Found %d chunk boundaries in the input file.", len(boundaries))
    logger.info("Using %d CPU cores for BPE training.", num_cores)

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [
            executor.submit(
                split_text_into_chunks,
                input_path,
                start,
                end,
            )
            for start, end in zip(boundaries[:-1], boundaries[1:])
        ]

        word_frequencies = defaultdict(int)

        for future in futures:
            chunk_frequencies = future.result()
            for word, freq in chunk_frequencies.items():
                word_frequencies[word] += freq

    logger.info("Total unique words found: %d", len(word_frequencies))

    splits = split_words(word_frequencies)
    logger.info("Total unique splits found: %d", len(splits))

    return train_bpe_tokenizer(
        splits,
        word_frequencies,
        vocab_size,
        [special_token.encode("utf-8") for special_token in special_tokens],
    )
