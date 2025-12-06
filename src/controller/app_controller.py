"""
Application Controller - Coordinates Model and View
"""

from PyQt5.QtWidgets import QFileDialog
from typing import Optional
from pathlib import Path

from ..model import LZ78Compressor, FileHandler, FileHandlerBinary


class AppController:
    """
    Main application controller.
    Handles communication between Model and View.
    """
    
    def __init__(self, view):
        self.view = view
        self.compressor = LZ78Compressor()
        self.file_handler = FileHandler()
        self.file_handler_binary = FileHandlerBinary()
        
        # Current file data
        self.current_file_path: Optional[str] = None
        self.current_text: Optional[str] = None
        self.compressed_data: Optional[list] = None
        self.dictionary: Optional[dict] = None
        self.decompressed_text: Optional[str] = None
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect view signals to controller methods."""
        # File loading
        self.view.btn_load_text.clicked.connect(self.load_text_file)
        self.view.btn_load_compressed.clicked.connect(self.load_compressed_file)
        
        # Compression
        self.view.btn_compress.clicked.connect(self.compress_file)
        self.view.btn_save_compressed.clicked.connect(self.save_compressed_file)
        
        # Decompression
        self.view.btn_decompress.clicked.connect(self.decompress_file)
        self.view.btn_save_decompressed.clicked.connect(self.save_decompressed_file)
    
    def load_text_file(self):
        """Load a text file for compression."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Seleccionar Archivo de Texto",
            "",
            "Archivos de Texto (*.txt);;Todos los Archivos (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            # Read file
            self.current_text = self.file_handler.read_text_file(file_path)
            self.current_file_path = file_path
            
            # Update view
            self.view.text_original.setPlainText(self.current_text)
            self.view.file_path_label.setText(Path(file_path).name)
            self.view.btn_compress.setEnabled(True)
            
            # Clear previous compression data
            self.view.text_compressed.clear()
            self.view.text_decompressed.clear()
            self.view.btn_save_compressed.setEnabled(False)
            
            self.view.show_success(f"Archivo cargado exitosamente: {Path(file_path).name}")
            
        except FileNotFoundError:
            self.view.show_error("Archivo No Encontrado", "El archivo seleccionado no existe.")
        except ValueError as e:
            self.view.show_error("Archivo Inválido", str(e))
        except Exception as e:
            self.view.show_error("Error", f"Error inesperado: {str(e)}")
    
    def load_compressed_file(self):
        """Load a compressed .lz78 file for decompression."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Seleccionar Archivo Comprimido",
            "",
            "Archivos LZ78 (*.lz78);;Todos los Archivos (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            # Load compressed file
            self.compressed_data, self.dictionary, original_filename = \
                self.file_handler_binary.load_compressed_file(file_path)
            
            self.current_file_path = file_path
            
            # Display compressed data
            compressed_display = "Datos Comprimidos (Índice, Carácter):\n\n"
            for idx, (index, char) in enumerate(self.compressed_data[:100]):  # Show first 100
                compressed_display += f"({index}, '{char}') "
                if (idx + 1) % 10 == 0:
                    compressed_display += "\n"
            
            if len(self.compressed_data) > 100:
                compressed_display += f"\n\n... ({len(self.compressed_data) - 100} entradas más)"
            
            self.view.text_compressed.setPlainText(compressed_display)
            self.view.file_path_label.setText(Path(file_path).name)
            self.view.btn_decompress.setEnabled(True)
            
            # Update dictionary display
            self.view.update_dictionary_display(self.dictionary)
            
            # Clear decompressed text
            self.view.text_decompressed.clear()
            
            self.view.show_success(f"Archivo comprimido cargado: {Path(file_path).name}")
            
        except FileNotFoundError:
            self.view.show_error("Archivo No Encontrado", "El archivo comprimido seleccionado no existe.")
        except ValueError as e:
            self.view.show_error("Archivo Inválido", str(e))
        except Exception as e:
            self.view.show_error("Error", f"Error inesperado: {str(e)}")
    
    def compress_file(self):
        """Compress the loaded text file."""
        if not self.current_text:
            self.view.show_error("Sin Archivo", "Por favor carga un archivo de texto primero.")
            return
        
        try:
            # Perform compression
            self.compressed_data, self.dictionary = self.compressor.compress(self.current_text)
            
            # Display compressed data
            compressed_display = "Datos Comprimidos (Índice, Carácter):\n\n"
            for idx, (index, char) in enumerate(self.compressed_data[:100]):  # Show first 100
                compressed_display += f"({index}, '{char}') "
                if (idx + 1) % 10 == 0:
                    compressed_display += "\n"
            
            if len(self.compressed_data) > 100:
                compressed_display += f"\n\n... ({len(self.compressed_data) - 100} entradas más)"
            
            self.view.text_compressed.setPlainText(compressed_display)
            
            # Update dictionary display
            self.view.update_dictionary_display(self.dictionary)
            
            # Calculate and display statistics
            filename = Path(self.current_file_path).name if self.current_file_path else 'temp.txt'
            stats = self.compressor.get_statistics(self.current_text, filename)
            self.view.update_statistics(stats)
            
            # Enable save button
            self.view.btn_save_compressed.setEnabled(True)
            
            self.view.show_success("¡Archivo comprimido exitosamente!")
            
        except Exception as e:
            self.view.show_error("Error de Compresión", f"Error durante la compresión: {str(e)}")
    
    def save_compressed_file(self):
        """Save compressed data to a .lz78 file."""
        if not self.compressed_data:
            self.view.show_error("Sin Datos", "Por favor comprime un archivo primero.")
            return
        
        # Suggest file name
        if self.current_file_path:
            suggested_name = Path(self.current_file_path).stem + ".lz78"
        else:
            suggested_name = "comprimido.lz78"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Guardar Archivo Comprimido",
            suggested_name,
            "Archivos LZ78 (*.lz78);;Todos los Archivos (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            original_filename = Path(self.current_file_path).name if self.current_file_path else "unknown.txt"
            self.file_handler_binary.save_compressed_file(
                file_path,
                self.compressed_data,
                self.dictionary,
                original_filename
            )
            
            self.view.show_success(f"Archivo comprimido guardado: {Path(file_path).name}")
            
        except Exception as e:
            self.view.show_error("Error al Guardar", f"Error al guardar archivo comprimido: {str(e)}")
    
    def decompress_file(self):
        """Decompress the loaded .lz78 file."""
        if not self.compressed_data or not self.dictionary:
            self.view.show_error("Sin Datos", "Por favor carga un archivo comprimido primero.")
            return
        
        try:
            # Perform decompression
            self.decompressed_text = self.compressor.decompress(
                self.compressed_data,
                self.dictionary
            )
            
            # Display decompressed text
            self.view.text_decompressed.setPlainText(self.decompressed_text)
            
            # Enable save button
            self.view.btn_save_decompressed.setEnabled(True)
            
            # Update statistics
            filename = Path(self.current_file_path).stem + '.txt' if self.current_file_path else 'temp.txt'
            stats = self.compressor.get_statistics(self.decompressed_text, filename)
            self.view.update_statistics(stats)
            
            self.view.show_success("¡Archivo descomprimido exitosamente!")
            
        except Exception as e:
            self.view.show_error("Error de Descompresión", f"Error durante la descompresión: {str(e)}")
    
    def save_decompressed_file(self):
        """Save decompressed text to a file."""
        if not self.decompressed_text:
            self.view.show_error("Sin Datos", "Por favor descomprime un archivo primero.")
            return
        
        # Suggest file name
        suggested_name = "descomprimido.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Guardar Archivo Descomprimido",
            suggested_name,
            "Archivos de Texto (*.txt);;Todos los Archivos (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            self.file_handler.save_text_file(file_path, self.decompressed_text)
            self.view.show_success(f"Archivo descomprimido guardado: {Path(file_path).name}")
            
        except Exception as e:
            self.view.show_error("Error al Guardar", f"Error al guardar archivo descomprimido: {str(e)}")
