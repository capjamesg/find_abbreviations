import os
import re
from collections import defaultdict
from typing import Tuple

# 10k words from https://www.mit.edu/~ecprice/wordlist.10000
with open("10k.txt") as f:
    tenk_words = f.read().split()

    tenk_words = set(tenk_words)

# input, result
tests = [
    [
        "Dancing With our Hands Tied (DWHT) is my favourite song.",
        ("Dancing With our Hands Tied", "DWoHT"),
    ],
    [
        "Dancing With Our Hands Tied (DWHT) is my favourite song.",
        ("Dancing With Our Hands Tied", "DWOHT"),
    ],
    [
        "Dancing With Our Hands Tied is my favourite song.",
        ("Dancing With Our Hands Tied", "DWOHT"),
    ],
    [
        "Dancing With Our Hands Tied (D.W.O.H.T) is my favourite song.",
        ("Dancing With Our Hands Tied", "DWOHT"),
    ],
    ["Club Penguin is a video game.", ("Club Penguin", "CP")],
]


def get_abbreviations_and_acronyms(
    text: str, lowercase_first_word=False
) -> Tuple[str, str]:
    """
    Given a string, return the longest abbreviation or acronym in the form of:

    - ... Word Like This (WLT) ... = ('Word Like This', 'WLT')
    - ... Word Like This ... = ('Word Like This', 'WLT')
    - ... Word Like This (W.L.T) ... = ('Word Like This', 'WLT')
    - ... Word like This (WLT) ... = ('Word Like This', 'WlT')

    Parameters:

    - text: str: The text to extract the abbreviation / acronym from.
    - lowercase_first_word: bool: Whether to lowercase the first word in the text.
        You may want to set this to True if the text is a sentence and you are unsure if you know the first word
        is not part of an abbreviation / acronym.
    """
    if lowercase_first_word:
        text = text[0].lower() + text[1:]

    abbreviations_with_symbol_structure = re.findall(
        r"([A-Z][a-z]+(?: [A-Z][a-z]+)+) \(([A-Z]+)\)", text
    )

    all_words = text.split()
    words = defaultdict(str)

    buffer = []

    for i, word in enumerate(all_words):
        if i == 0 and word.islower():
            continue

        if word.strip().islower() and (
            i < len(all_words) - 1 and all_words[i + 1][0].islower()
        ):
            continue

        # if all caps, skip
        # skip if next word starts with a capital letter
        if (
            i < len(all_words) - 1
            and (word.istitle() and all_words[i + 1][0].istitle())
            or (
                i < len(all_words) - 2
                and all_words[i + 1][0].islower()
                and all_words[i + 2][0].istitle()
            )
        ):
            buffer.append(word)
            continue

        # if next word is upper, continue
        if i < len(all_words) - 1 and all_words[i + 1].istitle():
            buffer.append(word)
            continue

        if len(buffer) > 0:
            # if current word starts with a capital
            if word[0].isupper():
                word = " ".join(buffer) + " " + word
            else:
                word = " ".join(buffer)

            word = word.strip()

            if not words.get(word):
                words[word] = "".join([c[0] for c in word.split(" ") if c.isalpha()])

    # get longest
    if not words:
        return []

    longest = [max(words, key=lambda x: len(x))]

    return (longest[0], words[longest[0]])


for test in tests:
    input, result = test
    output = get_abbreviations_and_acronyms(input)
    assert output == result, f"{output} != {result}"
