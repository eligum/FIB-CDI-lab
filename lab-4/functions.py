"""Lab4 implementation."""

from collections import Counter
import math

Token77 = tuple[int, int, str]
TokenSS = tuple[bool, str] | tuple[bool, int, int]
Token78 = tuple[int, str]
NOT_FOUND = -1

#####################################
# LZ77: sliding window dictionaries #
#####################################


def encode_LZ77(text: str, s: int, t: int) -> list[Token77]:
    """Encode a python string with the LZ77 algorithm.

    Parameters
    ----------
    text : Sequence of characters to be encoded.
    s : Search buffer length.
    t : Lookahead buffer length.
    """
    tokens = []
    curr_pos = 0  # window position (first index of the lookahead buffer)
    n = len(text)

    while curr_pos < n:
        # 1. Find the longest match
        w_begin = max(0, curr_pos - s)    # window first index
        w_end = min(n - 1, curr_pos + t)  # window last index + 1
        (index, length) = find_longest_match(text, curr_pos, w_begin, w_end)
        # 2. Append token
        offset = (curr_pos - index) if index != NOT_FOUND else 1
        symbol = text[curr_pos + length]
        token = (offset, length, symbol)
        tokens.append(token)
        # 3. Increase pointer
        curr_pos += length + 1

    return tokens


def decode_LZ77(tokens: list[Token77]) -> str:
    text = []

    for (offset, length, symbol) in tokens:
        if length > 0:
            for _ in range(length):
                text.append(text[-offset])
        text.append(symbol)

    return "".join(text)


def encode_LZSS(text: str, mm: int, s: int, t: int) -> list[TokenSS]:
    """Encode a python string with the LZSS algorithm.

    Parameters
    ----------
    text : Sequence of characters to be encoded.
    mm : Minimum match length.
    s : Search buffer length.
    t : Lookahead buffer length.
    """
    tokens = []
    curr_pos = 0  # window position (first index of the lookahead buffer)
    n = len(text)

    while curr_pos < n:
        # 1. Find the longest match
        w_begin = max(0, curr_pos - s)  # window first index
        w_end = min(n, curr_pos + t)    # window last index + 1
        (index, length) = find_longest_match(text, curr_pos, w_begin, w_end, mm)
        # 2. Append token
        if index != NOT_FOUND:
            offset = (curr_pos - index)
            token = (True, offset, length)
        else:
            token = (False, text[curr_pos])
            length = 1
        tokens.append(token)
        # 3. Increase pointer
        curr_pos += length

    return tokens


def decode_LZSS(tokens: list[TokenSS]) -> str:
    text = []

    for (bitflag, *args) in tokens:
        if not bitflag:
            text.append(args[0])
        else:
            offset, length = args
            for _ in range(length):
                text.append(text[-offset])

    return "".join(text)


##########################################################
# LZ78: diccionaris creats a partir de paraules del text #
##########################################################


def encode_LZ78(text: str) -> list[Token78]:
    """Encode a python string with the LZ78 algorithm.
    """
    tokens = []
    word_list = [""]
    curr_pos = 0
    n = len(text)

    while curr_pos < n:
        # Check if symbol at `curr_pos` has already been seen before
        index = None
        for (i, word) in enumerate(word_list):
            if word == text[curr_pos]:
                index = i
                break
        # If it has not, append token with index 0 and update `word_list`
        if index is None:
            tokens.append((0, text[curr_pos]))
            word_list.append(text[curr_pos])
            curr_pos += 1
        # If it has, search for a longer match in the dictionary with the next
        # symbol at `curr_pos` + k for k = 1, 2, 3... until no match is found.
        else:
            found = True
            w_end = curr_pos + 2
            while found and w_end <= n:
                found = False
                for (i, word) in enumerate(word_list[(index + 1):], index + 1):
                    if word == text[curr_pos:w_end]:
                        found = True
                        index = i
                        break
                w_end += 1
            # Check what caused the loop to terminate
            if found:
                tokens.append((index, ""))
            else:
                tokens.append((index, text[w_end - 2]))
            # Update dictionary and current position
            word_list.append(text[curr_pos:(w_end - 1)])
            curr_pos = w_end - 1

    return tokens


def decode_LZ78(tokens: list[Token78]) -> str:
    text = []
    word_list = [""]

    for (index, char) in tokens:
        text.append(word_list[index])
        text.append(char)
        word_list.append(word_list[index] + char)

    return "".join(text)


def encode_LZW(text: str):
    """Encode a python string with the LZW algorithm.
    """
    pass


def decode_LZW(tok):
    pass


##################################
# Altres: reordenacio de lletres #
##################################


def encode_burrows_wheeler(text: str):
    pass


def decode_burrows_wheeler(tok, alf):
    pass


def encode_move_to_front(text: str):
    pass


def decode_move_to_front(tok, alf):
    pass


#######################
# Auxiliary functions #
#######################


def find_longest_match(
    data: str,
    curr_pos: int,
    window_begin: int,
    window_end: int,
    min_match: int = 1
) -> tuple[int, int]:
    for word_end in range(window_end, curr_pos, -1):
        if word_end - curr_pos < min_match:
            break
        word = data[curr_pos:word_end]
        index = data.find(word, window_begin, word_end)
        if index < curr_pos:
            return (index, len(word))

    return (NOT_FOUND, 0)


#########
# Tests #
#########


if __name__ == "__main__":
    while True:
        text = input("Input string: ")
        tokens = encode_LZSS(text, 5, 100, 100)
        print(tokens)
        decode = decode_LZSS(tokens)
        print(decode)
