"""Lab2 code."""

from typing import List, Tuple
from collections import Counter
from utils import Timer
import random
import math


def source_from_text(text: str) -> List[Tuple[str, int]]:
    """Returns the frequency of each character in the string.
    """
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1

    return list(freq.items())


def encode(text: str, corr: List[Tuple[str, str]]) -> str:
    map_ab = dict(corr)
    i = 0
    j = 1
    result = []
    while j <= len(text):
        word = text[i:j]
        if word in map_ab:
            result.append(map_ab[word])
            i = j
        j += 1

    return "".join(result)


def decode(text: str, corr: List[Tuple[str, str]]) -> str:
    map_ba = {b: a for (a, b) in corr}
    i = 0
    j = 1
    result = []
    while j <= len(text):
        word = text[i:j]
        if word in map_ba:
            result.append(map_ba[word])
            i = j
        j += 1

    return "".join(result)


def canonical_code(lengths: List[int]) -> List[str]:
    """Returns the canonical prefix code over the alphabet `{0, 1}` associated
    to a list of integers.

    Each value in the input list represents the length of a codeword in the
    resulting code. This function will trigger an assertion if it is not
    possible to create a prefix code with the given list. If it succeeds, the
    codewords of the returned code will be sorted by lenght in the same order
    as in the input list.

    For example:

    >>> >>> canonical_code([3, 3, 2, 4])
    >>> ['010', '011', '00', '1000']
    """
    # Kraft-McMillan inequality
    assert sum(pow(2, -li) for li in lengths) <= 1

    counter = list(Counter(sorted(lengths)).items())
    code = []
    num = 0
    prev_len = counter[0][0]

    # Construct code in lexicographical order
    for (length, count) in counter:
        num = num << (length - prev_len)
        for _ in range(count):
            code.append(f"{num:0{length}b}")
            num += 1
        prev_len = length

    # Reorder codewords
    index = 0
    for length in lengths:
        for i in range(index, len(code)):
            if len(code[i]) == length:
                temp = code.pop(i)
                code.insert(index, temp)
                break
        index += 1

    return code


def increment_by_one(value, alf):
    n = len(alf)
    val_idx = len(value) - 1
    alf_idx = alf.index(value[val_idx])

    # Propagate increment if at last symbol of alphabet
    while alf_idx == (n - 1):
        value[val_idx] = alf[0]
        if val_idx == 0:
            value.insert(0, alf[1])
            return
        val_idx -= 1
        alf_idx = alf.index(value[val_idx])

    # Increment digit by one
    value[val_idx] = alf[alf_idx + 1]


def canonical_code_q(lengths: List[int], q: int, alf: List[str]) -> List[str]:
    """Returns the canonical prefix code over the alphabet `alf` associated
    to a list of integers.
    """
    # Kraft-McMillan inequality
    if not sum(pow(q, -li) for li in lengths) <= 1:
        print("Les longituds no satisfan Kraft-McMillan: no existeix cap codi")
        return

    counter = list(Counter(sorted(lengths)).items())
    code = []
    codeword = []

    # Construct code in lexicographical order
    for (length, count) in counter:
        for _ in range(length - len(codeword)):
            codeword.append(alf[0])
        for _ in range(count):
            code.append("".join(str(d) for d in codeword))
            increment_by_one(codeword, alf)

    # Reorder codewords
    index = 0
    for length in lengths:
        for i in range(index, len(code)):
            if len(code[i]) == length:
                temp = code.pop(i)
                code.insert(index, temp)
                break
        index += 1

    return code


def shannon_code(src: List[Tuple[str, int]]) -> List[str]:
    w = sum(wi for (_, wi) in src)
    lengths = [math.ceil(-math.log2(wi / w)) for (_, wi) in src]

    return canonical_code_q(lengths, 2, ['0', '1'])


def maximal_code_missing_lengths(lengths: List[int]) -> List[int]:
    max_len = max(lengths)

    total = pow(2, max_len)
    consumed = sum(pow(2, max_len - li) for li in lengths)
    remaining = total - consumed
    bin_rep = "{:b}".format(remaining)

    result = []
    for i, digit in enumerate(bin_rep):
        if digit == '1':
            result.append(i + 1)

    return result


if __name__ == "__main__":
    # t = Timer()

    # text = "0101110011110010"
    # t.start()
    # result = decode(encode(text, corr), corr)
    # t.stop()

    # source = [("a", 2), ("b", 2), ("c", 2), ("e", 4)]
    # print(shannon_code(source))
    # txt = open("../data/quijote_clean.txt", "r", encoding="utf-8").read()
    # src = source_from_text(txt[:1000])
    # print(shannon_code(src))

    # lens_1 = [3,2,5,6] #+ [1,4,6]
    # lens_2 = [9, 7, 9, 5, 13, 12, 5, 12, 9, 11, 7, 4, 8, 7] #+ [1, 2, 4, 6, 7, 8, 11, 12, 13]
    # res = maximal_code_missing_lengths(lens_1)
    # print(res)

    src = [
        (' ', 381208), ('a', 200499), ('b', 24147), ('c', 59437), ('d', 87240), ('e', 229191),
        ('f', 7581), ('g', 17225), ('h', 19920), ('i', 90077), ('j', 10530), ('l', 89143),
        ('m', 44658), ('n', 112683), ('o', 162514), ('p', 35465), ('q', 32483), ('r', 100955),
        ('s', 125728), ('t', 61749), ('u', 79560), ('v', 17856), ('w', 2), ('x', 377),
        ('y', 25115), ('z', 6491)
    ]

    code = shannon_code(src)
    corr = list(zip((k for (k, _) in src), code))

    text = "recluse as if when the ship had sailed from home nothing but the dead wintry bleakness of the sea had then kept him so secluded and by and by it came to pass that he was almost continually in the air but as yet for all that he said or perceptibly did on the at last sunny deck he seemed as unnecessary there as another mast but the pequod was only making a passage now not regularly cruising nearly all whaling preparatives needing supervision the mates were fully competent to so that there was little or nothing out of himself to employ or excite ahab now and thus chase away for that one interval the clouds that layer upon layer were piled upon his brow as ever all clouds choose the loftiest peaks to pile themselves upon nevertheless ere long the warm warbling persuasiveness of the pleasant holiday weather we came to seemed gradually to charm him from his mood for as when the red"
    enc_text = "1010010111110100001101010100000110001110100011010001000000110000100010110011100111000001001110101011000010011101111100000011000010001011001001110000010110011000101001011111010000110101010000001000010000011000111101000111110100010001000011010010010100000010010000010101100010011010011000011111000000001011001010000101011110010100000101000001000101100111010110000100010111101111011100001000000110110101100011101011000000101000011001000101011000010001011011001000100001001010001000010101001010000110100110111010010000110000100010110111110100010011001011000001001110010100001010010101100110111000000101010100011111010000100000010001011100000011001100010010101111101000100000100010111000100010011010000011111010010111000010101001000000110010101011100001010001010101000001001110010100001000100111010101001010000001001000011011011010110000100110011110000010101010001111101000010000001100011100001011000000101000001110001010000001111100101000100010011010001000110100111001110011011100100100010000100010110010010000001100100010000101100101000000111001111000100000100111001111010001011001110000000101010101111011000111001000000111110010100001010011001001011001010011100000011011101001000011000101010000110100101001001100110111000001000101100110001001110010011010011000001001110010100001001010011100111001001101001100010001100100010110111101111011011000100001100100010001000101000110001101011010001001110111110000001100010010001011001010000001010010001000011100000110010001010001100100100000011111001010000100010110011000100010011101100000110011100010001000100101010110000101011001111101000000100010100100000110010101110001100000100001001010111110000010010101100001010100001010000100000011011010001010100101000011010110100010101010111101111100000000101000111010111101100011010000010011010110100001011011001000100010010001111100111100000010010100011100010001011000000101000011000100000010110110010011100010101001010000100000100010100100000110010101110001100000100001001110011100111101010000111000000001111100101000010001011001100001011001010000001110011100010001100100010110111101111011010000010011100101000001011001110000000100100011111001111010101001001110011000111101110100010001000110100101100100111000001010000011111010000111001010000010110011100000001010010110001000101100000111010111100111000010101100000100011111010111000110111000001111100101000100100011110111010010000111000001110000100010111110011100110100011001001110011100010000110101100011101001100011100000110001110100110000100010111100001110001100101000000001011001110000000001001110010100001000101111000011010111101110100110000001010001000010001011001110011110001001101101101011110011100010000100011110001001010010011010110100000100001010101100000011101011000010010001011001010101010100001110000000100101001010001010000010010101100100010101100000100111001010000011010111101111100010011000100101011001000101011000010001011001100000100110101101101000100010110001111011100000100011110000100010110011000101001001001100100101000001001110010100001010010010011001001010001010101011110110100111000100001100011100000100010110011000011010010100010100000100100010110010101010101000011100000001010100101000010000001111011100011000011100011100100001110001100010110001000010010000111000100010001011111001110011000001010010010010001111101000011100100000011111001010000100010110011000011010010101001100010000010011100101000010000001110011010100001101001001000110001111011101000100001111100101000010001011001100010100101011001001101001100010010101100100010101100111000010101100000111110010100010100101011011001001000101100001000101100110001010010010011001001010001001110010101011000010101000011000010100011001110011100110101000001000101100110001001101000000100111001010000100011010110100111101010001111011010000010011100101000010101000010010101001100011000011000100000100101100000011101100000010100000110111001000110110101100000101100101010101101010100110111010001000010001011001001000001010010101100110111000010001001110101111001110000001001101000100010101101100101010110001000001010000001100010010010000101000011001000101100011101001100000110001110000100100011111001111010101001001110101011000000100001010010101100100110100110001001110010101011000010101000011000100010100100001010001001001010111000010101001010110000011110111000110001010111100111000110001001101101000010001011001101110000001110001100100001010101010011000001001110010100001010100001100010010101100011100010011010110110101100001010111001100011010110100110101000000100111001010000100100001010101010100101000100000011010100001010100101011000000100111001111010001011001110000"

    print(encode(text, corr))
    print(decode(enc_text, corr))
