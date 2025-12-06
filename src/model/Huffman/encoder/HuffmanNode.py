import heapq
from typing import Optional

class HuffmanNode:
    def __init__(self, char: Optional[str] = None, freq: int = 0):
        self.char: Optional[str] = char
        self.freq: int = freq
        self.left: Optional['HuffmanNode'] = None
        self.right: Optional['HuffmanNode'] = None

    # Required for priority queue (heapq)
    def __lt__(self, other: 'HuffmanNode') -> bool:
        return self.freq < other.freq