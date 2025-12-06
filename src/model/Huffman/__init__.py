"""
Huffman Package
---------------
A modular and extensible implementation of Huffman coding in Python.

This package provides all core functionalities required for Huffman text
compression, including encoding, decoding, entropy and efficiency analysis,
and file management for persistence of encoded data.

Functions
---------
Encode(message: str) -> Tuple[Dict[str, int], HuffmanNode, Dict[str, str], str]
    Executes the Huffman encoding process: counts character frequencies,
    builds the binary tree, generates symbol codes, and returns the encoded message.

Decode(encodedMessage: str, codesDict: Dict[str, str]) -> str
    Decodes a Huffman-encoded binary message back into its original text
    using the provided code dictionary.

Metrics(freqDict: Dict[str, int], codesDict: Dict[str, str]) -> Dict[str, float]
    Calculates and returns the entropy, average code length, and efficiency
    of the Huffman code.

Save(codesDict: Dict[str, str], encodedMessage: str, filename: str) -> None
    Saves the Huffman code dictionary and encoded message to a .txt file.

Load(filename: str) -> Tuple[Dict[str, str], str]
    Loads and reconstructs the Huffman code dictionary and encoded message
    from a .txt file previously generated with Save().
"""

from .encoder.encoder import Encode
from .decoder.decoder import Decode as Decode
from .metrics.metrics import Metrics
from .file.filemanager import SaveToTxt as Save, LoadFromTxt as Load

__all__ = ["Encode", "Decode", "Metrics", "Save", "Load"]
