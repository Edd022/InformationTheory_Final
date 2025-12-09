"""
Binary File Handler for LZ78 + Huffman hybrid compression
Optimized binary format with Huffman encoding support
"""

import struct
import pickle
from pathlib import Path
from typing import Tuple, List, Dict


class FileHandlerBinaryHuffman:
    """
    Handles file operations for LZ78 + Huffman hybrid compression.
    Format version 2 includes Huffman-encoded indices.
    """
    
    LZ78_EXTENSION = '.lz78'
    MAGIC_NUMBER = b'LZ7H'  # LZ78 + Huffman signature
    VERSION = 2
    
    @staticmethod
    def save_compressed_file(file_path: str, 
                            compressed_data: List[Tuple[int, str]], 
                            lz78_dictionary: Dict[str, int],
                            huffman_codes: Dict[str, str],
                            encoded_indices: str,
                            original_filename: str) -> None:
        """
        Save hybrid compressed data to binary .lz78 file.
        
        OPTIMIZACIÓN: NO guardamos el diccionario LZ78 completo.
        Se puede reconstruir durante la descompresión.
        
        Binary format (version 2 - optimized):
        - Magic number (4 bytes): 'LZ7H' (LZ78 + Huffman)
        - Version (1 byte): 2
        - Original filename length (2 bytes): uint16
        - Original filename (variable): UTF-8 encoded
        - Huffman codes count (4 bytes): uint32
        - Huffman codes: For each code:
            - Symbol length (2 bytes): uint16
            - Symbol (variable): UTF-8 encoded
            - Code length (2 bytes): uint16
            - Code (variable): UTF-8 encoded binary string
        - Encoded indices bit count (4 bytes): uint32
        - Encoded indices (variable): Packed bits
        - Characters count (4 bytes): uint32
        - Characters: For each character:
            - Char length (1 byte): uint8
            - Char (variable): UTF-8 encoded
        
        Args:
            file_path: Path where to save the compressed file
            compressed_data: List of (index, character) tuples from LZ78
            lz78_dictionary: LZ78 phrase dictionary (NOT SAVED - can be reconstructed)
            huffman_codes: Huffman codes for indices
            encoded_indices: Binary string of Huffman-encoded indices
            original_filename: Original file name
        """
        # Ensure .lz78 extension
        if not file_path.endswith(FileHandlerBinaryHuffman.LZ78_EXTENSION):
            file_path += FileHandlerBinaryHuffman.LZ78_EXTENSION
        
        try:
            with open(file_path, 'wb') as f:
                # Write magic number (LZ7H = LZ78 + Huffman)
                f.write(FileHandlerBinaryHuffman.MAGIC_NUMBER)
                
                # Write version (2)
                f.write(struct.pack('B', FileHandlerBinaryHuffman.VERSION))
                
                # Write original filename
                filename_bytes = original_filename.encode('utf-8')
                f.write(struct.pack('H', len(filename_bytes)))
                f.write(filename_bytes)
                
                # *** NO GUARDAMOS EL DICCIONARIO LZ78 - se reconstruye en descompresión ***
                
                # Write Huffman codes dictionary
                f.write(struct.pack('I', len(huffman_codes)))
                for symbol, code in huffman_codes.items():
                    symbol_bytes = symbol.encode('utf-8')
                    code_bytes = code.encode('utf-8')
                    f.write(struct.pack('H', len(symbol_bytes)))
                    f.write(symbol_bytes)
                    f.write(struct.pack('H', len(code_bytes)))
                    f.write(code_bytes)
                
                # Write Huffman-encoded indices
                bit_count = len(encoded_indices)
                f.write(struct.pack('I', bit_count))
                
                # Pack bits into bytes
                byte_array = bytearray()
                for i in range(0, bit_count, 8):
                    byte_chunk = encoded_indices[i:i+8]
                    # Pad with zeros if necessary
                    byte_chunk = byte_chunk.ljust(8, '0')
                    byte_value = int(byte_chunk, 2)
                    byte_array.append(byte_value)
                f.write(bytes(byte_array))
                
                # Write characters from compressed_data
                f.write(struct.pack('I', len(compressed_data)))
                for _, char in compressed_data:
                    char_bytes = char.encode('utf-8')
                    f.write(struct.pack('B', len(char_bytes)))
                    f.write(char_bytes)
                    
        except Exception as e:
            raise ValueError(f"Error saving hybrid compressed file: {str(e)}")
    
    @staticmethod
    def load_compressed_file(file_path: str) -> Tuple[List[Tuple[int, str]], Dict[str, int], Dict[str, str], str, str]:
        """
        Load a hybrid binary .lz78 compressed file.
        
        Args:
            file_path: Path to the .lz78 file
            
        Returns:
            Tuple of (compressed_data, lz78_dictionary, huffman_codes, encoded_indices, original_filename)
            Note: lz78_dictionary will be reconstructed, not loaded
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is incorrect
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                # Read and verify magic number
                magic = f.read(4)
                if magic != FileHandlerBinaryHuffman.MAGIC_NUMBER:
                    raise ValueError("Invalid file format: incorrect magic number")
                
                # Read version
                version = struct.unpack('B', f.read(1))[0]
                if version != 2:
                    raise ValueError(f"Unsupported format version: {version}")
                
                # Read original filename
                filename_length = struct.unpack('H', f.read(2))[0]
                original_filename = f.read(filename_length).decode('utf-8')
                
                # *** NO LEEMOS DICCIONARIO LZ78 - se reconstruye ***
                
                # Read Huffman codes
                huffman_size = struct.unpack('I', f.read(4))[0]
                huffman_codes = {}
                for _ in range(huffman_size):
                    symbol_length = struct.unpack('H', f.read(2))[0]
                    symbol = f.read(symbol_length).decode('utf-8')
                    code_length = struct.unpack('H', f.read(2))[0]
                    code = f.read(code_length).decode('utf-8')
                    huffman_codes[symbol] = code
                
                # Read Huffman-encoded indices
                bit_count = struct.unpack('I', f.read(4))[0]
                byte_count = (bit_count + 7) // 8
                byte_data = f.read(byte_count)
                
                # Unpack bytes into bit string
                encoded_indices = ''
                for byte in byte_data:
                    encoded_indices += format(byte, '08b')
                # Trim to actual bit count
                encoded_indices = encoded_indices[:bit_count]
                
                # Read characters
                char_count = struct.unpack('I', f.read(4))[0]
                characters = []
                for _ in range(char_count):
                    char_length = struct.unpack('B', f.read(1))[0]
                    char = f.read(char_length).decode('utf-8')
                    characters.append(char)
                
                # Decode Huffman indices
                import sys
                import os
                huffman_path = os.path.join(os.path.dirname(__file__), 'Huffman')
                if huffman_path not in sys.path:
                    sys.path.insert(0, huffman_path)
                from decoder.decoder import Decode as HuffmanDecode
                
                decoded_symbols = HuffmanDecode(encoded_indices, huffman_codes)
                
                # Parse decoded symbols back to indices
                indices = []
                i = 0
                while i < len(decoded_symbols):
                    char = decoded_symbols[i]
                    # Si es un carácter < 256, es un índice directo
                    if ord(char) < 256:
                        indices.append(ord(char))
                        i += 1
                    else:
                        # Es una representación de string, leer hasta encontrar no-dígito
                        num_str = ''
                        while i < len(decoded_symbols) and decoded_symbols[i].isdigit():
                            num_str += decoded_symbols[i]
                            i += 1
                        if num_str:
                            indices.append(int(num_str))
                
                # Reconstruct compressed_data tuples
                compressed_data = list(zip(indices, characters))
                
                # Reconstruct LZ78 dictionary dynamically during decompression
                # El diccionario se construye igual que durante la compresión
                lz78_dictionary = {}
                dict_index = 1
                
                # Crear diccionario inverso temporal para la reconstrucción
                temp_reverse_dict = {}
                
                for idx, char in compressed_data:
                    if idx == 0:
                        phrase = char
                    else:
                        # Obtener la frase padre del diccionario temporal
                        if idx in temp_reverse_dict:
                            phrase = temp_reverse_dict[idx] + char
                        else:
                            # Si no existe, es un error pero intentamos continuar
                            phrase = char
                    
                    # Agregar al diccionario
                    lz78_dictionary[phrase] = dict_index
                    temp_reverse_dict[dict_index] = phrase
                    dict_index += 1
                
                return compressed_data, lz78_dictionary, huffman_codes, encoded_indices, original_filename
                
        except Exception as e:
            raise ValueError(f"Error loading hybrid compressed file: {str(e)}")
    
    @staticmethod
    def get_compressed_size(compressed_data: List[Tuple[int, str]], 
                           lz78_dictionary: Dict[str, int],
                           huffman_codes: Dict[str, str],
                           encoded_indices: str,
                           original_filename: str) -> int:
        """
        Calculate the size of the hybrid compressed file without actually saving it.
        OPTIMIZED: No guardamos el diccionario LZ78, solo códigos Huffman.
        
        Returns:
            Size in bytes
        """
        size = 0
        
        # Magic number + version
        size += 4 + 1
        
        # Filename
        filename_bytes = original_filename.encode('utf-8')
        size += 2 + len(filename_bytes)
        
        # *** NO GUARDAMOS DICCIONARIO LZ78 - gran ahorro de espacio ***
        
        # Huffman codes
        size += 4
        for symbol, code in huffman_codes.items():
            symbol_bytes = symbol.encode('utf-8')
            code_bytes = code.encode('utf-8')
            size += 2 + len(symbol_bytes) + 2 + len(code_bytes)
        
        # Encoded indices
        bit_count = len(encoded_indices)
        byte_count = (bit_count + 7) // 8
        size += 4 + byte_count
        
        # Characters
        size += 4
        for _, char in compressed_data:
            char_bytes = char.encode('utf-8')
            size += 1 + len(char_bytes)
        
        return size
