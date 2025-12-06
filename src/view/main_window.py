"""
Main Window - PyQt5 GUI for LZ78 Compressor
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QFileDialog, 
                             QMessageBox, QGroupBox, QGridLayout, QProgressBar,
                             QTableWidget, QTableWidgetItem, QTabWidget, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from pathlib import Path


class MainWindow(QMainWindow):
    """
    Main application window with modern UI design.
    Provides interface for compression and decompression operations.
    """
    
    # Signals for controller communication
    compress_requested = pyqtSignal(str)
    decompress_requested = pyqtSignal(str)
    save_compressed_requested = pyqtSignal(str)
    save_decompressed_requested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Compresor LZ78 - Teoría de la Información")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # File selection section
        file_section = self.create_file_section()
        main_layout.addWidget(file_section)
        
        # Tabs for operations
        tabs = self.create_tabs()
        main_layout.addWidget(tabs)
        
        # Statistics section
        stats_section = self.create_statistics_section()
        main_layout.addWidget(stats_section)
        
        # Status bar
        self.statusBar().showMessage("Listo")
        
        # Apply modern styling
        self.apply_styles()
        
    def create_header(self) -> QWidget:
        """Create header section."""
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        header_widget.setLayout(header_layout)
        
        title = QLabel("Compresor de Archivos LZ78")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        
        subtitle = QLabel("Universidad Distrital Francisco José de Caldas")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        return header_widget
    
    def create_file_section(self) -> QGroupBox:
        """Create file selection section."""
        group = QGroupBox("Selección de Archivo")
        layout = QGridLayout()
        group.setLayout(layout)
        
        # File path display
        self.file_path_label = QLabel("Ningún archivo seleccionado")
        self.file_path_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        
        # Buttons
        self.btn_load_text = QPushButton("Cargar Archivo de Texto")
        self.btn_load_text.setIcon(QIcon.fromTheme("document-open"))
        
        self.btn_load_compressed = QPushButton("Cargar Archivo Comprimido (.lz78)")
        self.btn_load_compressed.setIcon(QIcon.fromTheme("document-open"))
        
        layout.addWidget(QLabel("Archivo Actual:"), 0, 0)
        layout.addWidget(self.file_path_label, 0, 1, 1, 2)
        layout.addWidget(self.btn_load_text, 1, 0)
        layout.addWidget(self.btn_load_compressed, 1, 1)
        
        return group
    
    def create_tabs(self) -> QTabWidget:
        """Create tabbed interface for compression/decompression."""
        tabs = QTabWidget()
        
        # Compression tab
        compress_tab = self.create_compression_tab()
        tabs.addTab(compress_tab, "Compresión")
        
        # Decompression tab
        decompress_tab = self.create_decompression_tab()
        tabs.addTab(decompress_tab, "Descompresión")
        
        # Dictionary tab
        dictionary_tab = self.create_dictionary_tab()
        tabs.addTab(dictionary_tab, "Diccionario")
        
        return tabs
    
    def create_compression_tab(self) -> QWidget:
        """Create compression tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Original text area
        original_group = QGroupBox("Texto Original")
        original_layout = QVBoxLayout()
        original_group.setLayout(original_layout)
        
        self.text_original = QTextEdit()
        self.text_original.setPlaceholderText("Carga un archivo de texto para comprimir...")
        self.text_original.setReadOnly(True)
        original_layout.addWidget(self.text_original)
        
        # Compressed data area
        compressed_group = QGroupBox("Datos Comprimidos")
        compressed_layout = QVBoxLayout()
        compressed_group.setLayout(compressed_layout)
        
        self.text_compressed = QTextEdit()
        self.text_compressed.setPlaceholderText("Los datos comprimidos aparecerán aquí...")
        self.text_compressed.setReadOnly(True)
        compressed_layout.addWidget(self.text_compressed)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_compress = QPushButton("Comprimir")
        self.btn_compress.setEnabled(False)
        self.btn_save_compressed = QPushButton("Guardar Archivo Comprimido")
        self.btn_save_compressed.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_compress)
        button_layout.addWidget(self.btn_save_compressed)
        
        # Add to main layout
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(original_group)
        splitter.addWidget(compressed_group)
        
        layout.addWidget(splitter)
        layout.addLayout(button_layout)
        
        return widget
    
    def create_decompression_tab(self) -> QWidget:
        """Create decompression tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Decompressed text area
        decompressed_group = QGroupBox("Texto Descomprimido")
        decompressed_layout = QVBoxLayout()
        decompressed_group.setLayout(decompressed_layout)
        
        self.text_decompressed = QTextEdit()
        self.text_decompressed.setPlaceholderText("Carga un archivo .lz78 para descomprimir...")
        self.text_decompressed.setReadOnly(True)
        decompressed_layout.addWidget(self.text_decompressed)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.btn_decompress = QPushButton("Descomprimir")
        self.btn_decompress.setEnabled(False)
        self.btn_save_decompressed = QPushButton("Guardar Archivo Descomprimido")
        self.btn_save_decompressed.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_decompress)
        button_layout.addWidget(self.btn_save_decompressed)
        
        layout.addWidget(decompressed_group)
        layout.addLayout(button_layout)
        
        return widget
    
    def create_dictionary_tab(self) -> QWidget:
        """Create dictionary visualization tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        label = QLabel("Estructura del Diccionario LZ78")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(label)
        
        self.dictionary_table = QTableWidget()
        self.dictionary_table.setColumnCount(2)
        self.dictionary_table.setHorizontalHeaderLabels(["Cadena", "Índice"])
        self.dictionary_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.dictionary_table)
        
        return widget
    
    def create_statistics_section(self) -> QGroupBox:
        """Create statistics display section."""
        group = QGroupBox("Estadísticas de Compresión")
        layout = QGridLayout()
        group.setLayout(layout)
        
        # Labels for statistics
        self.lbl_original_size = QLabel("0 bytes")
        self.lbl_compressed_size = QLabel("0 bytes")
        self.lbl_compression_ratio = QLabel("0%")
        self.lbl_dictionary_size = QLabel("0 entradas")
        
        # Add to layout
        layout.addWidget(QLabel("Tamaño Original:"), 0, 0)
        layout.addWidget(self.lbl_original_size, 0, 1)
        layout.addWidget(QLabel("Tamaño Comprimido:"), 0, 2)
        layout.addWidget(self.lbl_compressed_size, 0, 3)
        layout.addWidget(QLabel("Ratio de Compresión:"), 1, 0)
        layout.addWidget(self.lbl_compression_ratio, 1, 1)
        layout.addWidget(QLabel("Tamaño Diccionario:"), 1, 2)
        layout.addWidget(self.lbl_dictionary_size, 1, 3)
        
        return group
    
    def apply_styles(self):
        """Apply modern styling to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dcdde1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QTextEdit {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
                font-family: Consolas, Monaco, monospace;
            }
            QTableWidget {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QLabel {
                color: #2c3e50;
            }
            QTabWidget::pane {
                border: 1px solid #dcdde1;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QStatusBar {
                background-color: #34495e;
                color: white;
            }
        """)
    
    # UI Update Methods
    def update_dictionary_display(self, dictionary: dict):
        """Update dictionary table display."""
        self.dictionary_table.setRowCount(len(dictionary))
        for i, (string, index) in enumerate(sorted(dictionary.items(), key=lambda x: x[1])):
            self.dictionary_table.setItem(i, 0, QTableWidgetItem(string))
            self.dictionary_table.setItem(i, 1, QTableWidgetItem(str(index)))
    
    def update_statistics(self, stats: dict):
        """Update statistics display."""
        self.lbl_original_size.setText(f"{stats['original_size']} bytes")
        self.lbl_compressed_size.setText(f"{stats['compressed_size']} bytes")
        self.lbl_compression_ratio.setText(f"{stats['compression_ratio']}%")
        self.lbl_dictionary_size.setText(f"{stats['dictionary_size']} entradas")
    
    def show_error(self, title: str, message: str):
        """Show error message dialog."""
        QMessageBox.critical(self, title, message)
    
    def show_info(self, title: str, message: str):
        """Show information message dialog."""
        QMessageBox.information(self, title, message)
    
    def show_success(self, message: str):
        """Show success message in status bar."""
        self.statusBar().showMessage(message, 5000)
