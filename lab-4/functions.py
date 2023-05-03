"""Lab4 implementation."""

from collections import Counter
import math

Token77 = tuple[int, int, str]
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
        print
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


def encode_LZSS(text: str, mm, s, t):
    pass


def decode_LZSS(tokens):
    pass


##########################################################
# LZ78: diccionaris creats a partir de paraules del text #
##########################################################


def encode_LZ78(text: str):
    pass


def decode_LZ78(tok):
    pass


def encode_LZW(text: str):
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


def find_longest_match(data: str, curr_pos: int, window_begin: int, window_end: int) -> tuple[int, int]:
    for word_end in range(window_end, curr_pos, -1):
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
        tokens = encode_LZ77(text, 100, 100)
        print(tokens)
        decode = decode_LZ77(tokens)
        print(decode)

    # corr = [("0", "a"), ("10", "b"), ("11", "c")]
    # text = "".join(random.choices(["0", "1"], k=100))

    # t = Timer()

    # text = "0101110011110010"
    # t.start()
    # result = decode(encode(text, corr), corr)
    # t.stop()

    # print(text, result, sep="\n")

    # lenghts = [3, 4, 2, 2, 4, 4, 3]
    # print(canonical_code(lenghts))

    # source = [("a", 2), ("b", 2), ("c", 2), ("e", 4)]
    # print(shannon_code(source))
    # txt = open("../data/quijote_clean.txt", "r", encoding="utf-8").read()
    # src = source_from_text(txt)

    # out = canonical_code([81, 81, 12, 2, 3, 7, 6, 15, 9, 9, 9, 9, 21, 3, 5])
    # for s in out:
    #     print(s)
