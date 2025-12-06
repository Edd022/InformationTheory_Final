"""
Configuration settings for the LZ78 Compressor application
"""

import os
from pathlib import Path

# Application information
APP_NAME = "LZ78 Compressor"
APP_VERSION = "1.0.0"
ORGANIZATION = "Universidad Distrital Francisco José de Caldas"

# File extensions
COMPRESSED_FILE_EXTENSION = ".lz78"
SUPPORTED_TEXT_EXTENSIONS = [".txt", ".log", ".csv", ".json", ".xml"]

# Compression settings
MAX_DICTIONARY_SIZE = 65536  # Maximum dictionary size (can be adjusted)
ENCODING = "utf-8"

# UI settings
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1200
WINDOW_DEFAULT_HEIGHT = 800

# File paths
BASE_DIR = Path(__file__).parent
RESOURCES_DIR = BASE_DIR / "resources"
DOCS_DIR = BASE_DIR / "docs"

# Ensure directories exist
RESOURCES_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
