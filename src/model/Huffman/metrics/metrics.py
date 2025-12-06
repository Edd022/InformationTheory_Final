import math
from typing import Dict, Tuple


def CalculateEntropy(freqDict: Dict[str, int]) -> float:
    """
    Calculates the Shannon entropy (in bits per symbol) for a given frequency dictionary.
    Formula: H = -Σ(p_i * log2(p_i))
    """
    totalSymbols: int = sum(freqDict.values())
    entropy: float = 0.0

    for freq in freqDict.values():
        probability: float = freq / totalSymbols
        entropy -= probability * math.log2(probability)

    return entropy


def CalculateAverageLength(freqDict: Dict[str, int], codeDict: Dict[str, str]) -> float:
    """
    Calculates the average codeword length of a Huffman code.
    Formula: L = Σ(p_i * l_i)
    """
    totalSymbols: int = sum(freqDict.values())
    avgLength: float = 0.0

    for char, freq in freqDict.items():
        probability: float = freq / totalSymbols
        codeLength: int = len(codeDict[char])
        avgLength += probability * codeLength

    return avgLength


def CalculateEfficiency(entropy: float, avgLength: float) -> float:
    """
    Calculates the efficiency of the Huffman code.
    Formula: η = H / L
    If avgLength == 0, efficiency = 0 to avoid division by zero.
    """
    if avgLength == 0:
        return 0.0
    return entropy / avgLength


def Metrics(freqDict: Dict[str, int], codeDict: Dict[str, str]) -> Tuple[float, float, float]:
    """
    Calculates entropy, average length, and efficiency for a given Huffman code.
    Returns a tuple (entropy, averageLength, efficiency)
    """
    entropy: float = CalculateEntropy(freqDict)
    avgLength: float = CalculateAverageLength(freqDict, codeDict)
    efficiency: float = CalculateEfficiency(entropy, avgLength)

    return entropy, avgLength, efficiency


# Example usage
if __name__ == "__main__":
    # Example with the message "CASA"
    freqExample: Dict[str, int] = {'A': 2, 'C': 1, 'S': 1}
    codesExample: Dict[str, str] = {'A': '1', 'C': '00', 'S': '01'}

    entropy, avgLength, efficiency = Metrics(freqExample, codesExample)

    print(f"Entropy (H): {entropy:.4f} bits/symbol")
    print(f"Average Length (L): {avgLength:.4f} bits/symbol")
    print(f"Efficiency (η): {efficiency * 100:.2f}%")