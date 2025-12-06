"""
Test para analizar el problema de compresión
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.model import LZ78Compressor, FileHandler
import json


def analyze_compression_issue():
    """Analizar el problema de tamaño."""
    
    print("=" * 70)
    print("ANÁLISIS DEL PROBLEMA DE COMPRESIÓN LZ78")
    print("=" * 70)
    
    # Prueba 1: Texto pequeño
    print("\n📝 PRUEBA 1: Texto Pequeño (repetitivo)")
    text1 = "abababababababab"
    analyze_text(text1, "Texto pequeño repetitivo")
    
    # Prueba 2: Texto mediano
    print("\n📝 PRUEBA 2: Texto Mediano")
    text2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 5
    analyze_text(text2, "Texto mediano")
    
    # Prueba 3: Texto grande
    print("\n📝 PRUEBA 3: Texto Grande")
    text3 = "Esta es una prueba de compresión. " * 100
    analyze_text(text3, "Texto grande")
    
    # Prueba 4: Archivo de prueba existente
    print("\n📝 PRUEBA 4: Archivo test_sample.txt")
    try:
        file_handler = FileHandler()
        text4 = file_handler.read_text_file("test_sample.txt")
        analyze_text(text4, "test_sample.txt")
    except:
        print("No se pudo leer test_sample.txt")


def analyze_text(text, name):
    """Analizar un texto específico."""
    print(f"\n🔍 Analizando: {name}")
    print(f"   Longitud: {len(text)} caracteres")
    
    # Comprimir
    compressor = LZ78Compressor()
    compressed_data, dictionary = compressor.compress(text)
    
    # Calcular tamaños REALES
    original_bytes = len(text.encode('utf-8'))
    
    # Tamaño de datos comprimidos en JSON
    compressed_data_json = json.dumps(compressed_data)
    compressed_data_bytes = len(compressed_data_json.encode('utf-8'))
    
    # Tamaño del diccionario en JSON
    dictionary_json = json.dumps(dictionary)
    dictionary_bytes = len(dictionary_json.encode('utf-8'))
    
    # Tamaño total del archivo .lz78 (con metadata)
    full_file = {
        'original_filename': 'test.txt',
        'compressed_data': compressed_data,
        'dictionary': dictionary,
        'version': '1.0'
    }
    full_file_json = json.dumps(full_file, ensure_ascii=False, separators=(',', ':'))
    full_file_bytes = len(full_file_json.encode('utf-8'))
    
    # Calcular ratios
    ratio_actual = ((original_bytes - full_file_bytes) / original_bytes * 100) if original_bytes > 0 else 0
    
    # Mostrar resultados
    print(f"\n   📊 TAMAÑOS:")
    print(f"      Original:              {original_bytes:>6} bytes")
    print(f"      Datos comprimidos:     {compressed_data_bytes:>6} bytes")
    print(f"      Diccionario:           {dictionary_bytes:>6} bytes")
    print(f"      Archivo .lz78 TOTAL:   {full_file_bytes:>6} bytes")
    print(f"      Overhead JSON:         {full_file_bytes - compressed_data_bytes - dictionary_bytes:>6} bytes")
    
    print(f"\n   📈 ANÁLISIS:")
    print(f"      Entradas diccionario:  {len(dictionary)}")
    print(f"      Tuplas comprimidas:    {len(compressed_data)}")
    print(f"      Ratio REAL:            {ratio_actual:>6.2f}%")
    
    if full_file_bytes > original_bytes:
        print(f"      ⚠️  EXPANSIÓN: +{full_file_bytes - original_bytes} bytes ({abs(ratio_actual):.2f}% más grande)")
    else:
        print(f"      ✅ COMPRESIÓN: -{original_bytes - full_file_bytes} bytes ({ratio_actual:.2f}% reducción)")
    
    # Verificar descompresión
    decompressed = compressor.decompress(compressed_data, dictionary)
    if decompressed == text:
        print("      ✓ Descompresión correcta")
    else:
        print("      ✗ ERROR en descompresión")


if __name__ == "__main__":
    analyze_compression_issue()
