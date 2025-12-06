"""
decoder.py
-----------

This module provides the Huffman decoding functionality.

Functions
---------
Decode(encodedMessage: str, codesDict: Dict[str, str]) -> str
    Decodes a binary Huffman-encoded string into its original text
    using the provided Huffman code dictionary.
"""

from typing import Dict


def Decode(encodedMessage: str, codesDict: Dict[str, str]) -> str:
    """
    Decodes a binary Huffman-encoded string into its original text.

    Parameters
    ----------
    encodedMessage : str
        The binary string representing the encoded message.
    codesDict : Dict[str, str]
        The Huffman dictionary mapping each symbol to its binary code.

    Returns
    -------
    str
        The decoded original message.
    """
    # Invert dictionary: binary code → symbol
    inverseDict: Dict[str, str] = {code: symbol for symbol, code in codesDict.items()}

    decodedText: str = ""
    buffer: str = ""

    # Read bit by bit and match to symbols
    for bit in encodedMessage:
        buffer += bit
        if buffer in inverseDict:
            decodedText += inverseDict[buffer]
            buffer = ""

    return decodedText
