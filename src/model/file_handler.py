"""
File Handler for reading and writing compressed files
"""

import json
import os
from pathlib import Path
from typing import Tuple, List, Dict, Optional


class FileHandler:
    """
    Handles file operations for compression and decompression.
    Manages .lz78 file format and text file I/O.
    """
    
    LZ78_EXTENSION = '.lz78'
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        Read a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Content of the file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or not readable
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Not a valid file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content:
                raise ValueError("File is empty")
                
            return content
            
        except UnicodeDecodeError:
            raise ValueError("File is not readable as text (encoding error)")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
    
    @staticmethod
    def save_compressed_file(file_path: str, compressed_data: List[Tuple[int, str]], 
                            dictionary: Dict[str, int], original_filename: str) -> None:
        """
        Save compressed data to .lz78 file.
        
        Args:
            file_path: Path where to save the compressed file
            compressed_data: List of (index, character) tuples
            dictionary: Compression dictionary
            original_filename: Original file name
        """
        # Ensure .lz78 extension
        if not file_path.endswith(FileHandler.LZ78_EXTENSION):
            file_path += FileHandler.LZ78_EXTENSION
        
        data = {
            'original_filename': original_filename,
            'compressed_data': compressed_data,
            'dictionary': dictionary,
            'version': '1.0'
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        except Exception as e:
            raise ValueError(f"Error saving compressed file: {str(e)}")
    
    @staticmethod
    def load_compressed_file(file_path: str) -> Tuple[List[Tuple[int, str]], Dict[str, int], str]:
        """
        Load a .lz78 compressed file.
        
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
        
        if not file_path.endswith(FileHandler.LZ78_EXTENSION):
            raise ValueError(f"Incompatible file format. Expected {FileHandler.LZ78_EXTENSION}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            required_keys = ['compressed_data', 'dictionary', 'original_filename']
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Invalid file format: missing '{key}'")
            
            # Convert dictionary keys back to strings and values to integers
            dictionary = {str(k): int(v) for k, v in data['dictionary'].items()}
            
            # Convert compressed data tuples
            compressed_data = [(int(item[0]), str(item[1])) for item in data['compressed_data']]
            
            return compressed_data, dictionary, data['original_filename']
            
        except json.JSONDecodeError:
            raise ValueError("Invalid file format: not a valid JSON file")
        except Exception as e:
            raise ValueError(f"Error loading compressed file: {str(e)}")
    
    @staticmethod
    def save_text_file(file_path: str, content: str) -> None:
        """
        Save decompressed text to a file.
        
        Args:
            file_path: Path where to save the text file
            content: Text content to save
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise ValueError(f"Error saving text file: {str(e)}")
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """
        Validate if a file path is valid and accessible.
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            path = Path(file_path)
            return path.parent.exists() and path.parent.is_dir()
        except:
            return False
