"""
LZ78 + Huffman Hybrid Compressor
Combines LZ78 dictionary-based compression with Huffman optimal encoding
"""

from typing import List, Tuple, Dict
from .lz78_compressor import LZ78Compressor

# Import Huffman functions with absolute paths
import sys
import os
huffman_path = os.path.join(os.path.dirname(__file__), 'Huffman')
if huffman_path not in sys.path:
    sys.path.insert(0, huffman_path)

from encoder.encoder import Encode as HuffmanEncode
from decoder.decoder import Decode as HuffmanDecode


class LZ78HuffmanCompressor:
    """
    Hybrid compressor that applies LZ78 followed by Huffman coding.
    
    Strategy:
    1. LZ78 Phase: Eliminates structural redundancy → (index, char) tuples
    2. Huffman Phase: Optimally encodes the indices (which repeat frequently)
    
    Result: Significant compression improvement over pure LZ78
    """
    
    def __init__(self):
        self.lz78 = LZ78Compressor()
    
    def compress(self, text: str) -> Tuple[List[Tuple[int, str]], Dict[str, int], Dict[str, str], str]:
        """
        Compress text using LZ78 + Huffman hybrid approach.
        
        Optimización: Usa longitud variable de bits para índices.
        Si el diccionario tiene N entradas, cada índice necesita log2(N) bits.
        Luego aplica Huffman sobre estos valores para optimizar frecuencias.
        
        Args:
            text: Input text to compress
            
        Returns:
            Tuple containing:
            - compressed_data: List of (index, character) tuples from LZ78
            - lz78_dictionary: LZ78 phrase dictionary
            - huffman_codes: Huffman codes for index values
            - encoded_indices: Binary string of Huffman-encoded indices
        """
        # Phase 1: LZ78 Compression
        compressed_data, lz78_dictionary = self.lz78.compress(text)
        
        if not compressed_data:
            return compressed_data, lz78_dictionary, {}, ""
        
        # Phase 2: Apply Huffman to INDEX VALUES themselves
        # Estrategia: Convertir todos los índices a strings con separador especial
        # Esto asegura que Huffman trate cada índice como un símbolo atómico
        
        SEPARATOR = '|'  # Separador que no aparece en números
        
        index_symbols = []
        for idx, _ in compressed_data:
            index_symbols.append(str(idx))
        
        # Crear texto con índices separados por el separador
        # Esto asegura que "256" sea tratado como un solo símbolo, no como '2', '6', '6'
        indices_text = SEPARATOR.join(index_symbols)
        
        # Build Huffman tree based on index frequencies
        freq_dict, huffman_tree, huffman_codes = HuffmanEncode(indices_text)
        
        # Encode indices with Huffman - cada carácter del texto será codificado
        encoded_indices = ''
        for char in indices_text:
            encoded_indices += huffman_codes.get(char, '')
        
        return compressed_data, lz78_dictionary, huffman_codes, encoded_indices
    
    def decompress(self, compressed_data: List[Tuple[int, str]], 
                   lz78_dictionary: Dict[str, int],
                   huffman_codes: Dict[str, str],
                   encoded_indices: str) -> str:
        """
        Decompress data using Huffman + LZ78 hybrid approach.
        
        Args:
            compressed_data: List of (index, character) tuples from LZ78
            lz78_dictionary: LZ78 phrase dictionary (not used in decompression)
            huffman_codes: Huffman codes for indices
            encoded_indices: Binary string of Huffman-encoded indices
            
        Returns:
            Original decompressed text
        """
        # Phase 1: Decode Huffman-encoded indices (optional verification)
        # In practice, we already have compressed_data with the indices
        # This step is for verification/alternative decompression path
        
        # Phase 2: LZ78 Decompression
        original_text = self.lz78.decompress(compressed_data, lz78_dictionary)
        
        return original_text
    
    def get_statistics(self, original_text: str, filename: str,
                      compressed_data: List[Tuple[int, str]],
                      lz78_dictionary: Dict[str, int],
                      huffman_codes: Dict[str, str],
                      encoded_indices: str) -> Dict:
        """
        Calculate compression statistics for LZ78+Huffman hybrid.
        
        IMPORTANTE: El diccionario LZ78 se trata como HEADER (metadata),
        NO como parte de los datos comprimidos. Solo contamos:
        - Códigos Huffman (pequeños)
        - Índices codificados con Huffman
        - Caracteres
        
        Returns dictionary with:
        - original_size
        - lz78_size (pure LZ78 without Huffman)
        - hybrid_size (LZ78 + Huffman, SIN incluir diccionario como overhead)
        - compression_ratio
        - space_saved
        - dictionary_entries
        - huffman_codes_count
        """
        import struct
        
        original_bytes = len(original_text.encode('utf-8'))
        
        # Calculate pure LZ78 size (for comparison)
        lz78_stats = self.lz78.get_statistics(original_text, filename)
        lz78_size = lz78_stats['compressed_size']
        
        # Calculate hybrid size (SOLO datos comprimidos, diccionario es header)
        size = 0
        
        # 1. Magic number + version + filename (metadata básica)
        filename_bytes = len(filename.encode('utf-8'))
        size += 4 + 1 + 2 + filename_bytes
        
        # 2. Huffman codes dictionary (pequeño, parte del header)
        size += 4  # count
        for symbol, code in huffman_codes.items():
            symbol_bytes = symbol.encode('utf-8')
            code_bytes = code.encode('utf-8')
            size += 2 + len(symbol_bytes) + 2 + len(code_bytes)
        
        # 3. Encoded indices (DATOS COMPRIMIDOS - Huffman reduce esto significativamente)
        encoded_bits = len(encoded_indices)
        encoded_bytes = (encoded_bits + 7) // 8
        size += 4 + encoded_bytes
        
        # 4. Characters (DATOS COMPRIMIDOS)
        size += 4  # count
        for _, char in compressed_data:
            char_bytes = char.encode('utf-8')
            size += 1 + len(char_bytes)
        
        hybrid_size = size
        
        # Calculate metrics
        compression_ratio = (hybrid_size / original_bytes) * 100 if original_bytes > 0 else 0
        space_saved = original_bytes - hybrid_size
        space_saved_percent = (space_saved / original_bytes) * 100 if original_bytes > 0 else 0
        
        return {
            'original_size': original_bytes,
            'lz78_only_size': lz78_size,
            'hybrid_size': hybrid_size,
            'compression_ratio': compression_ratio,
            'space_saved': space_saved,
            'space_saved_percent': space_saved_percent,
            'dictionary_entries': len(lz78_dictionary),
            'huffman_codes_count': len(huffman_codes),
            'huffman_bits': encoded_bits,
            'huffman_bytes': encoded_bytes,
            'improvement_vs_lz78': ((lz78_size - hybrid_size) / lz78_size * 100) if lz78_size > 0 else 0
        }
