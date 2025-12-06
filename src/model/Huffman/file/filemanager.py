"""
file.py
-------

This module handles saving and loading data related to Huffman encoding
in a plain-text (.txt) format for human readability.

Functions:
----------
SaveToTxt(filePath: str, codesDict: Dict[str, str], encodedMessage: str) -> None
    Saves the Huffman dictionary and encoded message to a text file.

LoadFromTxt(filePath: str) -> Tuple[Dict[str, str], str]
    Loads the Huffman dictionary and encoded message from a text file.
"""

from typing import Dict, Tuple


def SaveToTxt(filePath: str, codesDict: Dict[str, str], encodedMessage: str) -> None:
    """
    Saves the Huffman dictionary and encoded message to a text file.

    Parameters
    ----------
    filePath : str
        Path to the output .txt file.
    codesDict : Dict[str, str]
        Dictionary mapping symbols to their Huffman codes.
    encodedMessage : str
        The final encoded message represented as a binary string.
    """
    with open(filePath, "w", encoding="utf-8") as file:
        file.write("--- HUFFMAN DICTIONARY ---\n")
        for symbol, code in codesDict.items():
            file.write(f"{symbol}: {code}\n")

        file.write("\n--- ENCODED MESSAGE ---\n")
        file.write(encodedMessage + "\n")


def LoadFromTxt(filePath: str) -> Tuple[Dict[str, str], str]:
    """
    Loads the Huffman dictionary and encoded message from a text file.

    Parameters
    ----------
    filePath : str
        Path to the .txt file containing Huffman data.

    Returns
    -------
    Tuple[Dict[str, str], str]
        A tuple containing:
        - The Huffman code dictionary
        - The encoded message
    """
    codesDict: Dict[str, str] = {}
    encodedMessage: str = ""

    with open(filePath, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    readingCodes = False
    readingMessage = False

    for line in lines:
        if line.startswith("--- HUFFMAN DICTIONARY ---"):
            readingCodes = True
            readingMessage = False
            continue
        elif line.startswith("--- ENCODED MESSAGE ---"):
            readingCodes = False
            readingMessage = True
            continue

        if readingCodes and ":" in line:
            symbol, code = line.split(":", 1)
            codesDict[symbol.strip()] = code.strip()
        elif readingMessage:
            encodedMessage += line.strip()

    return codesDict, encodedMessage
