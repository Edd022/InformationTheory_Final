"""
LZ78 Compression Algorithm Implementation
"""

from typing import List, Tuple, Dict


class LZ78Compressor:
    """
    Implements the LZ78 compression algorithm.
    Handles compression and decompression of text data.
    """
    
    def __init__(self):
        self.dictionary: Dict[str, int] = {}
        self.compressed_data: List[Tuple[int, str]] = []
        self.dictionary_size: int = 0
        
    def compress(self, text: str) -> Tuple[List[Tuple[int, str]], Dict[str, int]]:
        """
        Compress text using LZ78 algorithm.
        
        Args:
            text: Input text to compress
            
        Returns:
            Tuple containing compressed data and dictionary
        """
        self.dictionary = {}
        self.compressed_data = []
        self.dictionary_size = 0
        
        current_string = ""
        
        for char in text:
            combined = current_string + char
            
            if combined in self.dictionary:
                current_string = combined
            else:
                # Add to dictionary
                self.dictionary_size += 1
                self.dictionary[combined] = self.dictionary_size
                
                # Output (index, char)
                index = self.dictionary.get(current_string, 0)
                self.compressed_data.append((index, char))
                
                current_string = ""
        
        # Handle remaining string
        if current_string:
            index = self.dictionary.get(current_string[:-1], 0) if len(current_string) > 1 else 0
            self.compressed_data.append((index, current_string[-1]))
            
        return self.compressed_data, self.dictionary
    
    def decompress(self, compressed_data: List[Tuple[int, str]], dictionary: Dict[str, int]) -> str:
        """
        Decompress data using LZ78 algorithm.
        
        Args:
            compressed_data: List of (index, character) tuples
            dictionary: Dictionary used during compression
            
        Returns:
            Decompressed text
        """
        # Reverse dictionary for decompression
        reverse_dict = {v: k for k, v in dictionary.items()}
        decompressed = ""
        
        for index, char in compressed_data:
            if index == 0:
                phrase = char
            else:
                phrase = reverse_dict[index] + char
            
            decompressed += phrase
            
        return decompressed
    
    def get_dictionary(self) -> Dict[str, int]:
        """Return the current dictionary."""
        return self.dictionary
    
    def get_compressed_data(self) -> List[Tuple[int, str]]:
        """Return the compressed data."""
        return self.compressed_data
    
    def get_statistics(self, original_text: str, original_filename: str = 'temp.txt') -> Dict[str, any]:
        """
        Calculate compression statistics using binary format.
        
        Args:
            original_text: Original uncompressed text
            original_filename: Name of the original file (for accurate size calculation)
            
        Returns:
            Dictionary with statistics
        """
        from .file_handler_binary import FileHandlerBinary
        
        original_size = len(original_text.encode('utf-8'))
        
        # Calculate REAL compressed size using binary format
        compressed_size = FileHandlerBinary.get_compressed_size(
            self.compressed_data,
            self.dictionary,
            original_filename
        )
        
        # Calculate compression ratio (negative means expansion)
        compression_ratio = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
        
        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': round(compression_ratio, 2),
            'dictionary_size': len(self.dictionary)
        }
