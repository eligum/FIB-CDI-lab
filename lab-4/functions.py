"""Lab3 code."""

from typing import List, Tuple
from collections import Counter
from utils import Timer
import random
import math

##########################################
# LZ77: diccionaris de finestra lliscant #
##########################################


def encode_LZ77(text: str, s, t):
    pass


def decode_LZ77(tok):
    pass


def encode_LZSS(text: str, mm, s, t):
    pass


def decode_LZSS(tok):
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


# def source_from_text(text: str) -> List[Tuple[str, int]]:
#     """Returns the frequency of each character in the string.
#     """
#     freq = {}
#     for c in text:
#         freq[c] = freq.get(c, 0) + 1

#     return list(freq.items())


# def encode(text: str, corr: List[Tuple[str, str]]) -> str:
#     map_ab = dict(corr)
#     i = 0
#     j = 1
#     result = []
#     while j <= len(text):
#         word = text[i:j]
#         if word in map_ab:
#             result.append(map_ab[word])
#             i = j
#         j += 1

#     return "".join(result)


# def decode(text: str, corr: List[Tuple[str, str]]) -> str:
#     map_ba = {b: a for (a, b) in corr}
#     i = 0
#     j = 1
#     result = []
#     while j <= len(text):
#         word = text[i:j]
#         if word in map_ba:
#             result.append(map_ba[word])
#             i = j
#         j += 1

#     return "".join(result)


# def canonical_code(lengths: List[int]) -> List[str]:
#     """Returns the canonical prefix code over the alphabet `{0, 1}` associated
#     to a list of integers.

#     Each value in the input list represents the length of a codeword in the
#     resulting code. This function will trigger an assertion if it is not
#     possible to create a prefix code with the given list. If it succeeds, the
#     codewords of the returned code will be sorted by lenght in the same order
#     as in the input list.

#     For example:

#     >>> >>> canonical_code([3, 3, 2, 4])
#     >>> ['010', '011', '00', '1000']
#     """
#     # Kraft-McMillan inequality
#     assert sum(pow(2, -li) for li in lengths) <= 1

#     counter = list(Counter(sorted(lengths)).items())
#     code = []
#     num = 0
#     prev_len = counter[0][0]

#     # Construct code in lexicographical order
#     for (length, count) in counter:
#         num = num << (length - prev_len)
#         for _ in range(count):
#             code.append(f"{num:0{length}b}")
#             num += 1
#         prev_len = length

#     # Reorder codewords
#     index = 0
#     for length in lengths:
#         for i in range(index, len(code)):
#             if len(code[i]) == length:
#                 temp = code.pop(i)
#                 code.insert(index, temp)
#                 break
#         index += 1

#     return code


# def shannon_code(src: List[Tuple[str, int]]) -> List[str]:
#     w = sum(wi for (_, wi) in src)
#     assert w <= 1
#     lengths = [math.ceil(-math.log2(wi / w)) for (_, wi) in src]

#     return canonical_code(lengths)


# if __name__ == "__main__":
#     # corr = [("0", "a"), ("10", "b"), ("11", "c")]
#     # text = "".join(random.choices(["0", "1"], k=100))

#     # t = Timer()

#     # text = "0101110011110010"
#     # t.start()
#     # result = decode(encode(text, corr), corr)
#     # t.stop()

#     # print(text, result, sep="\n")

#     # lenghts = [3, 4, 2, 2, 4, 4, 3]
#     # print(canonical_code(lenghts))

#     # source = [("a", 2), ("b", 2), ("c", 2), ("e", 4)]
#     # print(shannon_code(source))
#     txt = open("../data/quijote_clean.txt", "r", encoding="utf-8").read()
#     src = source_from_text(txt)

#     out = canonical_code([81, 81, 12, 2, 3, 7, 6, 15, 9, 9, 9, 9, 21, 3, 5])
#     for s in out:
#         print(s)
