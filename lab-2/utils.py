from typing import List, Any, Iterable
from typing_extensions import Self
import time


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def elapsed(self) -> float:
        return time.perf_counter() - self._start_time

    def stop(self):
        if self._start_time is None:
            return

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")


class Tree:
    def __init__(self, data: Any, children: Iterable = None):
        self.data = data
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __str__(self, indent=0):
        others = []
        for child in self.children:
            others.append(child.__str__(indent + 2))
        return "\n".join([(" " * indent) + f"Tree({self.data})"] + others)

    def add_child(self, node):
        """Appends a node to the list of children of the current `Tree` node.
        """
        assert isinstance(node, Tree)
        self.children.append(node)

    def ith_child(self, index):
        return self.children[index]

    def is_leaf(self) -> bool:
        return not bool(self.children)

    def __iter__(self):
        queue = [self]
        while not len(queue) == 0:
            node = queue.pop(0)
            yield node.data
            for child in node.children:
                queue.append(child)

    @staticmethod
    def from_prefix_code(code: List[str]) -> Self:
        """Constructs a `Tree` from a list of words of a prefix code.
        """
        root = Tree(None)

        for word in code:
            curr_node = root
            for symbol in word:
                # Check if the current node has a child with the current
                # symbol, if not, insert a new child.
                for child in curr_node.children:
                    if child.data == symbol:
                        curr_node = child
                        break
                else:
                    new_node = Tree(symbol)
                    curr_node.add_child(new_node)
                    curr_node = new_node

        return root


# def encode_v2(text: str, corr: List[Tuple[str, str]]) -> str:
#     map_ab = dict(corr)
#     root = Tree.from_prefix_code(list(map_ab.keys()))
#     node = root
#     result = []
#     word = []

#     for char in text:
#         if node.is_leaf():
#             result.append(map_ab["".join(word)])
#             word.clear()
#             node = root

#         for child in node.children:
#             if child.data == char:
#                 word.append(char)
#                 node = child
#                 break

#     return "".join(result)


if __name__ == "__main__":
    t = Tree(1)
    t.add_child(Tree(2))
    t.add_child(Tree(3))
    t.add_child(Tree(4))
    t.ith_child(0).add_child(Tree(5))
    my_iter = iter(t)
    print([next(my_iter) for _ in range(4)])
    print([x for x in t])
    print(next(iter(t)))

    t = Tree.from_prefix_code(["0001", "0010", "10", "11"])
    print(t)
