"""
Binary File Handler for LZ78 compression
Optimized binary format for better compression ratios
"""

import struct
from pathlib import Path
from typing import Tuple, List, Dict


class FileHandlerBinary:
    """
    Handles file operations using optimized binary format.
    Significantly reduces file size compared to JSON format.
    """
    
    LZ78_EXTENSION = '.lz78'
    MAGIC_NUMBER = b'LZ78'  # File signature
    VERSION = 1
    
    @staticmethod
    def save_compressed_file(file_path: str, compressed_data: List[Tuple[int, str]], 
                            dictionary: Dict[str, int], original_filename: str) -> None:
        """
        Save compressed data to binary .lz78 file.
        
        Binary format:
        - Magic number (4 bytes): 'LZ78'
        - Version (1 byte): Format version
        - Original filename length (2 bytes): uint16
        - Original filename (variable): UTF-8 encoded
        - Dictionary size (4 bytes): uint32
        - Dictionary entries: For each entry:
            - String length (2 bytes): uint16
            - String (variable): UTF-8 encoded
            - Index (4 bytes): uint32
        - Compressed data count (4 bytes): uint32
        - Compressed data: For each tuple:
            - Index (4 bytes): uint32
            - Character (1-4 bytes): UTF-8 encoded char
        
        Args:
            file_path: Path where to save the compressed file
            compressed_data: List of (index, character) tuples
            dictionary: Compression dictionary
            original_filename: Original file name
        """
        # Ensure .lz78 extension
        if not file_path.endswith(FileHandlerBinary.LZ78_EXTENSION):
            file_path += FileHandlerBinary.LZ78_EXTENSION
        
        try:
            with open(file_path, 'wb') as f:
                # Write magic number
                f.write(FileHandlerBinary.MAGIC_NUMBER)
                
                # Write version
                f.write(struct.pack('B', FileHandlerBinary.VERSION))
                
                # Write original filename
                filename_bytes = original_filename.encode('utf-8')
                f.write(struct.pack('H', len(filename_bytes)))
                f.write(filename_bytes)
                
                # Write dictionary
                f.write(struct.pack('I', len(dictionary)))
                for string, index in dictionary.items():
                    string_bytes = string.encode('utf-8')
                    f.write(struct.pack('H', len(string_bytes)))
                    f.write(string_bytes)
                    f.write(struct.pack('I', index))
                
                # Write compressed data
                f.write(struct.pack('I', len(compressed_data)))
                for index, char in compressed_data:
                    f.write(struct.pack('I', index))
                    char_bytes = char.encode('utf-8')
                    f.write(struct.pack('B', len(char_bytes)))
                    f.write(char_bytes)
                    
        except Exception as e:
            raise ValueError(f"Error saving compressed file: {str(e)}")
    
    @staticmethod
    def load_compressed_file(file_path: str) -> Tuple[List[Tuple[int, str]], Dict[str, int], str]:
        """
        Load a binary .lz78 compressed file.
        
        Args:
            file_path: Path to the .lz78 file
            
        Returns:
            Tuple of (compressed_data, dictionary, original_filename)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is incorrect
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Compressed file not found: {file_path}")
        
        if not file_path.endswith(FileHandlerBinary.LZ78_EXTENSION):
            raise ValueError(f"Incompatible file format. Expected {FileHandlerBinary.LZ78_EXTENSION}")
        
        try:
            with open(file_path, 'rb') as f:
                # Read and verify magic number
                magic = f.read(4)
                if magic != FileHandlerBinary.MAGIC_NUMBER:
                    raise ValueError("Invalid file format: magic number mismatch")
                
                # Read version
                version = struct.unpack('B', f.read(1))[0]
                if version != FileHandlerBinary.VERSION:
                    raise ValueError(f"Unsupported file version: {version}")
                
                # Read original filename
                filename_length = struct.unpack('H', f.read(2))[0]
                original_filename = f.read(filename_length).decode('utf-8')
                
                # Read dictionary
                dict_size = struct.unpack('I', f.read(4))[0]
                dictionary = {}
                for _ in range(dict_size):
                    string_length = struct.unpack('H', f.read(2))[0]
                    string = f.read(string_length).decode('utf-8')
                    index = struct.unpack('I', f.read(4))[0]
                    dictionary[string] = index
                
                # Read compressed data
                data_count = struct.unpack('I', f.read(4))[0]
                compressed_data = []
                for _ in range(data_count):
                    index = struct.unpack('I', f.read(4))[0]
                    char_length = struct.unpack('B', f.read(1))[0]
                    char = f.read(char_length).decode('utf-8')
                    compressed_data.append((index, char))
                
                return compressed_data, dictionary, original_filename
                
        except struct.error as e:
            raise ValueError(f"Invalid file format: corrupted data ({str(e)})")
        except UnicodeDecodeError as e:
            raise ValueError(f"Invalid file format: encoding error ({str(e)})")
        except Exception as e:
            raise ValueError(f"Error loading compressed file: {str(e)}")
    
    @staticmethod
    def get_compressed_size(compressed_data: List[Tuple[int, str]], 
                           dictionary: Dict[str, int], 
                           original_filename: str) -> int:
        """
        Calculate the size of the compressed file in bytes without actually saving it.
        
        Args:
            compressed_data: List of (index, character) tuples
            dictionary: Compression dictionary
            original_filename: Original file name
            
        Returns:
            Size in bytes
        """
        size = 0
        
        # Magic number (4 bytes) + Version (1 byte)
        size += 4 + 1
        
        # Original filename
        filename_bytes = original_filename.encode('utf-8')
        size += 2 + len(filename_bytes)  # length (2) + data
        
        # Dictionary
        size += 4  # dictionary size (4 bytes)
        for string in dictionary.keys():
            string_bytes = string.encode('utf-8')
            size += 2 + len(string_bytes) + 4  # length (2) + data + index (4)
        
        # Compressed data
        size += 4  # data count (4 bytes)
        for _, char in compressed_data:
            char_bytes = char.encode('utf-8')
            size += 4 + 1 + len(char_bytes)  # index (4) + char_length (1) + char
        
        return size
