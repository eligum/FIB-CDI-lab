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
            offset = curr_pos - index
            token = (offset, length)
        else:
            token = text[curr_pos]
            length = 1
        tokens.append(token)
        # 3. Increase pointer
        curr_pos += length

    return tokens


def decode_LZSS(tokens: list[TokenSS]) -> str:
    text = []

    for tok in tokens:
        if type(tok) is str:
            text.append(tok)
        else:
            offset, length = tok
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
    codebook = [""]
    curr_pos = 0
    n = len(text)

    while curr_pos < n:
        # Check if symbol at `curr_pos` has already been seen before
        index = None
        for (i, word) in enumerate(codebook):
            if word == text[curr_pos]:
                index = i
                break
        # If it has not, append token with index 0 and update `codebook`
        if index is None or curr_pos == (n - 1):
            tokens.append((0, text[curr_pos]))
            codebook.append(text[curr_pos])
            curr_pos += 1
        # If it has, search for a longer match in the dictionary with the next
        # symbol at `curr_pos` + k for k = 1, 2, 3... until no match is found.
        else:
            found = True
            w_end = curr_pos + 2
            while w_end < n:
                found = False
                for (i, word) in enumerate(codebook[(index + 1):], index + 1):
                    if word == text[curr_pos:w_end]:
                        found = True
                        index = i
                        break
                if found:
                    w_end += 1
                else:
                    break
            # Append token with the pointer and the last unmatched symbol
            tokens.append((index, text[w_end - 1]))
            # Update dictionary and current position
            codebook.append(text[curr_pos:w_end])
            curr_pos = w_end

    return tokens


def decode_LZ78(tokens: list[Token78]) -> str:
    text = []
    word_list = [""]

    for (index, char) in tokens:
        text.append(word_list[index])
        text.append(char)
        word_list.append(word_list[index] + char)

    return "".join(text)


def encode_LZW(text: str) -> tuple[list[int], list[str]]:
    """Encode a python string with the LZW algorithm.
    """
    tokens = []
    curr_pos = 0
    n = len(text)
    # 1. Initialize dictionary to contain all strings of length one.
    alphabet = sorted(list(set(text)))
    codebook = alphabet.copy()

    while curr_pos < n:
        # 2. Find the longest matching substring of text `W` in the codebook.
        index = codebook.index(text[curr_pos])
        found = True
        w_end = curr_pos + 2
        while w_end <= n:
            found = False
            for (i, word) in enumerate(codebook[(index + 1):], index + 1):
                if word == text[curr_pos:w_end]:
                    found = True
                    index = i
                    break
            if found:
                w_end += 1
            else:
                break
        # 3. Emit the codebook index for `W` to output.
        tokens.append(index)
        # 4. Add `W` followed by the next symbol in the input to the codebook.
        if not found:
            codebook.append(text[curr_pos:w_end])
        # 5. Set `curr_pos` to the index of the next unencoded symbol.
        curr_pos = w_end - 1

    return (tokens, alphabet)


def decode_LZW(tokens: list[int], alf: list[str]) -> str:
    """Decode list of LZW tokens into a python string.

    See https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch#Decoding
    for more details.

    Parameters
    ----------
    tokens : List of pointers to dictionary entries.
    alf : Initial dictionary provided by the encoder.
    """
    codebook = alf.copy()
    prev_word = codebook[tokens[0]]
    output = [prev_word]

    for ptr in tokens[1:]:
        # A) The entry pointed at by `ptr` is already in the codebook.
        if ptr < len(codebook):
            word = codebook[ptr]
            output.append(word)
            codebook.append(prev_word + word[0])
            prev_word = word
        # B) The entry pointed at by `ptr` is not in the codebook yet.
        else:
            word = prev_word + prev_word[0]
            output.append(word)
            codebook.append(word)
            prev_word = word

    return "".join(output)


##################################
# Altres: reordenacio de lletres #
##################################


def encode_burrows_wheeler(text: str) -> tuple[str, int]:
    circular_shifts = []
    permutation = text

    for _ in range(len(text)):
        circular_shifts.append(permutation)
        permutation = permutation[1:] + permutation[0]

    circular_shifts.sort()
    output = [perm[-1] for perm in circular_shifts]

    return "".join(output), circular_shifts.index(text)


def decode_burrows_wheeler(codi: str, index: int) -> str:
    n = len(codi)
    table = [""] * n  # Initialize table of size N of empty rows

    for _ in range(n):
        for i in range(n):
            table[i] = codi[i] + table[i]
        table.sort()

    return table[index]


def encode_move_to_front(text: str) -> tuple[list[int], list[str]]:
    alphabet = sorted(list(set(text)))
    codebook = alphabet.copy()
    tokens = []

    for char in text:
        rank = codebook.index(char)  # Find rank of the current character
        tokens.append(rank)
        # Update codebook (move last encoded character to the front)
        codebook.pop(rank)
        codebook.insert(0, char)

    return (tokens, alphabet)


def decode_move_to_front(codi: list[int], alf: list[str]) -> str:
    codebook = alf.copy()
    text = []

    for rank in codi:
        text.append(codebook[rank])
        # Update codebook
        e = codebook.pop(rank)
        codebook.insert(0, e)

    return "".join(text)


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
        index = data.rfind(word, window_begin, word_end - 1)
        if index != NOT_FOUND:
            return (index, len(word))

    return (NOT_FOUND, 0)


def comp_lists(l1, l2):
    for i, (a, b) in enumerate(zip(l1, l2)):
        if a != b:
            print(f"[{i}] {a} --- {b}")
    print(f"Lengths: {len(l1)} --- {len(l2)}")


#########
# Tests #
#########


if __name__ == "__main__":
    # txt1 = "Setze jutges d'un jutjat mengen fetge d'un penjat."

    # text = txt1
    # tok = encode_LZSS(text, 3, 4096, 16)
    # print(tok)
    # assert text == decode_LZSS(tok)

    text = 3 * "a" + "xyz" + 5 * "b" + "xyz" + 3 * "c" + "xyz" + 5 * "d"
    tok, alf = encode_LZW(text)
    print(tok)
    assert text == decode_LZW(tok, alf)
