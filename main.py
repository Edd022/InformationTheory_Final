"""
LZ78 File Compressor Application
Universidad Distrital Francisco José de Caldas
Teoría de la Información - 2025

Main entry point for the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.view import MainWindow
from src.controller import AppController


def main():
    """Initialize and run the application."""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("LZ78 Compressor")
    app.setOrganizationName("Universidad Distrital")
    
    # Create main window
    window = MainWindow()
    
    # Create controller
    controller = AppController(window)
    
    # Show window
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
