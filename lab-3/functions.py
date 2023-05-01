"""Lab3 implementation."""

import math
import itertools
import heapq
from collections import Counter

Source = list[tuple[str, int | float]]
Code = dict[str, str]


class HuffmanTree:
    def __init__(self, info=None, left=None, right=None):
        self.left = left
        self.right = right
        self.info = info

    @staticmethod
    def _get_code(node, codeword: str = '') -> Code:
        """Returns the binary code for the given Huffman tree.
        """
        if node is None:
            return {}

        # Each node either has both children (the recursion must continue) or
        # none (it is a leaf node).
        if node.left is None:
            return {node.info: codeword}

        result = dict()
        result.update(HuffmanTree._get_code(node.left, codeword + '0'))
        result.update(HuffmanTree._get_code(node.right, codeword + '1'))

        return result

    def get_huffman_code(self, canonical: bool = True) -> Code:
        """Returns the binary code for this Huffman tree.
        """
        result = HuffmanTree._get_code(self)

        if canonical:
            # Sort by codeword length and then by key lexicographically in
            # increasing order.
            code = sorted(result.items(), key=lambda t: (len(t[1]), t[0]))
            keys = []
            lens = []
            for (k, v) in code:
                keys.append(k)
                lens.append(len(v))

            codewords = self._binary_canonical_code(lens)
            result = dict(zip(keys, codewords))

        return result

    def _binary_canonical_code(self, lengths: list[int]) -> list[str]:
        """Returns the binary prefix code based on the given list of codeword lengths.

        This is an optimized version that skips a lot of checks because the
        input list is assumed to have certain guarantees. For example, it
        assumes that the list is ordered increasingly and that the lengths
        satisfy the Kraft-McMillan inequality.
        """
        counter = list(Counter(lengths).items())
        codewords = []
        num = 0
        prev_length = counter[0][0]

        for (length, count) in counter:
            num = num << (length - prev_length)
            for _ in range(count):
                codewords.append(f"{num:0{length}b}")
                num += 1
            prev_length = length

        return codewords

    @staticmethod
    def build_tree(src: Source):
        """Constructs a Huffman tree from a source.

        The source is expected to be sorted increasingly in lexicographical
        order by key.
        """
        # Prioritize reversed insertion order to break ties. Tuples are
        # compared position by position: the first item of the first tuple is
        # compared to the first item of the second tuple; if they are equal the
        # second item is considered, then the third and so on.
        # The later and element is popped from the queue the shorter its
        # codeword is going to be.
        pq = [(f, len(src) - i, HuffmanTree(c)) for (i, (c, f)) in enumerate(src)]
        heapq.heapify(pq)

        root = HuffmanTree()
        while len(pq) > 1:
            (f1, _, node_l) = heapq.heappop(pq)
            (f2, _, node_r) = heapq.heappop(pq)
            root = HuffmanTree(None, node_l, node_r)
            heapq.heappush(pq, (f1 + f2, 0, root))

        return root


######################
# Auxilary functions #
######################

def entropy_pd(pmf: list[float]):
    """Given a probability mass function (pmf) return its entropy.
    """
    acum = 0.0
    for p_i in pmf:
        if p_i != 0:
            acum += p_i * -math.log2(p_i)

    return acum


def source_from_text(text: str, k: int = 1, pre: str = "") -> Source:
    """Returns the frequency of each block in the string.

    `k` is the number of characters from the `text` that are considered to be a block.
    `pre` is the prefix that every block must have in order to be considered one.
    """
    freq = dict()
    pre_len = len(pre)
    n = len(text)
    i = 0
    j = 0

    while j < n:
        if pre != "":
            i = text.find(pre, i)
            if i < 0:
                break
        j = i + pre_len + k
        if j <= n:
            block = text[(i + pre_len):j]
            freq[block] = freq.get(block, 0) + 1
        i += 1

    return sorted(freq.items())


def source_extension(src: Source, k: int) -> Source:
    """Returns a new source which is the extension of the given source `src`
    for a certain `k` value.
    """
    source = dict(src)
    symbols = source.keys()
    result = []

    products = [''.join(comb) for comb in itertools.product(symbols, repeat=k)]

    for prod in products:
        probability = 1
        for e in prod:
            probability *= source[e]
        result.append((prod, probability))

    return result


####################
# Actual functions #
####################

def entropy(text: str, k: int = 1, pre: str = ""):
    freq = source_from_text(text, k, pre)
    total = sum(freq.values())
    weights = [fi / total for fi in freq.values()]

    return entropy_pd(weights)


def mean_length(src: Source, code: list[str]):
    w_total = sum(w_i for (_, w_i) in src)
    acum = 0

    for word, p in zip(code, (wi for (_, wi) in src)):
        acum += len(word) * p

    return acum / w_total


def huffman_code(src: Source):
    tree = HuffmanTree.build_tree(src)

    return tree.get_huffman_code()


def arithmetic_encode(text: str, k: int) -> str:
    pass


def arithmetic_decode(code: Code, k: int, src: Source, length: int) -> str:
    pass


#########
# Tests #
#########

if __name__ == "__main__":
    text = "0000000001"
    src = source_from_text(text)
    src = source_extension(src, 3)
    print(src)

    tree = HuffmanTree.build_tree(src)
    print('--- Huffman code')
    code = tree.get_huffman_code(False)
    for (k, v) in sorted(code.items()):
        print(f"{k} -> {v}")
    print('--- Canonical Huffman code')
    code = tree.get_huffman_code(True)
    for (k, v) in sorted(code.items()):
        print(f"{k} -> {v}")
