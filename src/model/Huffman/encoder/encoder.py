from typing import Dict, Tuple, Any, List, Optional
import heapq

from .HuffmanNode import HuffmanNode

def CountCharacters(text: str) -> Dict[str, int]:
    """
    Counts the frequency of each character in the given text.
    Returns a dictionary sorted in descending order of frequency.
    """
    frequencyDict: Dict[str, int] = {}
    for char in text:
        frequencyDict[char] = frequencyDict.get(char, 0) + 1

    # Sort from higher to lower frequency
    sortedDict = dict(sorted(frequencyDict.items(), key=lambda item: item[1], reverse=True))
    return sortedDict


def BuildHuffmanTree(freqDict: Dict[str, int]) -> Optional[HuffmanNode]:
    """
    Builds the Huffman tree using the frequency dictionary.
    The rightmost (lowest frequency) nodes are combined first.
    Returns None if the frequency dictionary is empty.
    """
    if not freqDict:
        return None
        
    # Create initial nodes list sorted from rightmost (lowest freq)
    sortedItems = list(freqDict.items())[::-1]  # reverse for rightmost processing
    nodes: List[HuffmanNode] = [HuffmanNode(char, freq) for char, freq in sortedItems]

    # Turn list into a heap (min-heap)
    heapq.heapify(nodes)

    # Build Huffman Tree
    while len(nodes) > 1:
        # Extract two nodes with lowest frequency
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        # Create new internal node
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(nodes, merged)

    return nodes[0]  # root node


def GenerateHuffmanCodes(root: HuffmanNode) -> Dict[str, str]:
    """
    Traverses the Huffman tree and generates binary codes for each character.
    Left = '0', Right = '1'.
    """
    codes: Dict[str, str] = {}

    def Traverse(node: Optional[HuffmanNode], currentCode: str):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = currentCode
            return
        Traverse(node.left, currentCode + "0")
        Traverse(node.right, currentCode + "1")

    Traverse(root, "")
    return codes


def Encode(text: str) -> Tuple[Dict[str, int], HuffmanNode, Dict[str, str]]:
    """
    Main function that executes the 3 Huffman steps:
    1. Count characters
    2. Build tree
    3. Generate codes
    Returns a tuple: (frequency dictionary, tree root, codes dictionary)
    """
    freqDict = CountCharacters(text)
    treeRoot = BuildHuffmanTree(freqDict)
    codesDict = GenerateHuffmanCodes(treeRoot)
    return freqDict, treeRoot, codesDict



# Example test with message "CASA"
if __name__ == "__main__":
    text = "CASA"
    freq, tree, codes = Encode(text)

    print("Frequency Dictionary:", freq)
    print("Generated Huffman Codes:", codes)