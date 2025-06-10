from typing import DefaultDict, List, Dict, Optional, Tuple
from collections import defaultdict
from cs336_basics.bpe.pretokenization import split_text_into_iterator
from copy import deepcopy


def count_word_frequencies(text: str) -> DefaultDict[bytes, int]:
    word_frequencies = defaultdict(int)

    for match in split_text_into_iterator(text):
        word: str = match.group(0).strip()
        if word.strip():
            word_frequencies[word.encode("utf-8")] += 1

    return word_frequencies


def split_words(word_frequencies: DefaultDict[bytes, int]) -> Dict[bytes, List[bytes]]:
    return {
        word: [c.to_bytes(1, signed=False) for c in word]
        for word in word_frequencies.keys()
    }


def get_alphabet(word_frequencies: DefaultDict[bytes, int]) -> List[bytes]:
    alphabet = []

    for word in word_frequencies.keys():
        for byte in word:
            if byte not in alphabet:
                alphabet.append(byte)
    alphabet.sort()
    return alphabet


def compute_pair_freqs(
    splits: Dict[bytes, List[bytes]], word_frequencies: Dict[bytes, int]
) -> Dict[tuple, int]:
    pair_freqs = defaultdict(int)
    for word, freq in word_frequencies.items():
        split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            pair_freqs[pair] += freq
    return pair_freqs


def merge_pair(
    first_word: bytes,
    second_word: bytes,
    splits: Dict[bytes, List[bytes]],
    word_frequencies: Dict[bytes, int],
) -> None:
    """
    Merges the pair of words (first_word, second_word) in the splits and word_frequencies dictionaries.
    """
    for word in word_frequencies:
        split = splits[word]
        if len(split) == 1:
            continue

        i = 0
        while i < len(split) - 1:
            if split[i] == first_word and split[i + 1] == second_word:
                split = split[:i] + [first_word + second_word] + split[i + 2 :]
            else:
                i += 1
        splits[word] = split


def train_bpe_tokenizer(
    initial_splits: Dict[bytes, List[bytes]],
    word_frequencies: Dict[bytes, int],
    vocab_size: int,
    special_tokens: Optional[List[bytes]] = None,
    num_iterations: int = 10000,
) -> Tuple[Dict[int, bytes], List[Tuple[bytes, bytes]]]:
    merges = {}
    vocab = []
    if special_tokens is not None:
        for token in special_tokens:
            merges[token] = token
            vocab.append(token)

    splits = deepcopy(initial_splits)
    current_iteration = 0

    while len(vocab) < vocab_size and current_iteration < num_iterations:
        current_iteration += 1
        pair_freqs = compute_pair_freqs(splits, word_frequencies)

        best_pair = None
        max_freq = None
        for pair, freq in pair_freqs.items():
            if max_freq is None or max_freq < freq:
                best_pair = pair
                max_freq = freq
        if best_pair is None:
            break
        first_word, second_word = best_pair
        merge_pair(first_word, second_word, splits, word_frequencies)

        merges[best_pair] = first_word + second_word
        vocab.append(first_word + second_word)
    return {i: token for i, token in enumerate(vocab)}, list(merges.keys())
