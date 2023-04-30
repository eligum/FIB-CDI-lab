"""Lab3 implementation."""

import math
import itertools
import heapq

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
            # Sort by codeword length and then by key lexicographically
            code = sorted(result.items(), key=lambda t: (len(t[1]), t[0]))
            print(code)
            result = {k: v for (k, v) in zip(iter('abcd'), range(4))}

        return result

    @staticmethod
    def build_tree(src: Source):
        """Constructs a Huffman tree from a source.
        """
        # Remember insertion order to break ties. Tuples are compared position
        # by position: the first item of the first tuple is compared to the
        # first item of the second tuple; if they are equal the second item is
        # considered, then the third and so on.
        pq = [(f, i, HuffmanTree(c)) for (i, (c, f)) in enumerate(src)]
        heapq.heapify(pq)

        root = HuffmanTree()
        while len(pq) > 1:
            (f1, o1, node_l) = heapq.heappop(pq)
            (f2, o2, node_r) = heapq.heappop(pq)
            root = HuffmanTree(None, node_l, node_r)
            heapq.heappush(pq, (f1 + f2, min(o1, o2), root))

        return root


######################
# Auxilary functions #
######################

def entropy_pd(pd: list[float]):
    """Given a probability distribution (pd) returns its entropy.
    """
    acum = 0.0
    for p_i in pd:
        if p_i != 0:
            acum += p_i * -math.log2(p_i)

    return acum


def source_from_text(text: str, k: int = 1, pre: str = "") -> Source:
    """Returns the frequency of each block in the string.

    `k` is the number of characters from the `text` that are considered to be a block.
    `pre` is the prefix that every block must have in yhr dyting to be considered one.
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


#########
# Tests #
#########

if __name__ == "__main__":
    text = "ccdabbb"
    src = source_from_text(text)
    # src = source_extension(src, 2)
    print(src)
    tree = HuffmanTree.build_tree(src)
    code = tree.get_huffman_code()
    print(code)
