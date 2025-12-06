"""
Script de prueba para compresión de archivos de código fuente
Verifica la compresión efectiva en diferentes formatos
"""

import sys
import os

# Añadir src al path del proyecto
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

from model.lz78_huffman_compressor import LZ78HuffmanCompressor

def format_bytes(bytes_size):
    """Formatear bytes en unidades legibles"""
    if bytes_size < 1024:
        return f"{bytes_size:>7} bytes"
    elif bytes_size < 1024*1024:
        return f"{bytes_size/1024:>7.2f} KB"
    else:
        return f"{bytes_size/(1024*1024):>7.2f} MB"

def test_file(file_path, description):
    """Prueba compresión de un archivo"""
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return
    
    print(f"\nProbando: {os.path.basename(file_path)}")
    print(f"Tipo: {description}")
    print("-" * 70)
    
    # Leer archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_size = len(text.encode('utf-8'))
    print(f"Tamaño original: {format_bytes(original_size)}")
    
    # Comprimir
    compressor = LZ78HuffmanCompressor()
    compressed_data, lz78_dict, huffman_codes, encoded_indices = compressor.compress(text)
    
    # Calcular estadísticas
    stats = compressor.get_statistics(
        text, os.path.basename(file_path),
        compressed_data, lz78_dict,
        huffman_codes, encoded_indices
    )
    
    print(f"Tamaño comprimido: {format_bytes(stats['hybrid_size'])}")
    
    if stats['hybrid_size'] < stats['original_size']:
        reduction = stats['original_size'] - stats['hybrid_size']
        percentage = (reduction / stats['original_size']) * 100
        print(f"COMPRESIÓN EXITOSA: {format_bytes(reduction)} ({percentage:.2f}%)")
        print(f"Ratio: {stats['compression_ratio']:.2f}:1")
    else:
        increase = stats['hybrid_size'] - stats['original_size']
        percentage = (increase / stats['original_size']) * 100
        print(f"EXPANSIÓN: {format_bytes(increase)} ({percentage:.2f}%)")
    
    print(f"Entradas diccionario: {stats['dictionary_entries']:,}")
    print(f"Códigos Huffman: {stats['huffman_codes_count']}")
    
    # Verificar descompresión
    decompressed = compressor.decompress(
        compressed_data, lz78_dict,
        huffman_codes, encoded_indices
    )
    
    if decompressed == text:
        print("Descompresión: PERFECTA (100% exacta)")
    else:
        print("Descompresión: ERROR")

def main():
    print("=" * 70)
    print("PRUEBA DE COMPRESIÓN - ARCHIVOS DE CÓDIGO FUENTE".center(70))
    print("=" * 70)
    
    # Directorio de datos de prueba
    sample_data_dir = os.path.join(os.path.dirname(__file__), 'sample_data')
    
    # Archivos de prueba
    test_files = [
        (os.path.join(sample_data_dir, "large_code.py"), "Código Python grande (50 KB)"),
        (os.path.join(sample_data_dir, "example_code.py"), "Código Python (6.5 KB)"),
        (os.path.join(sample_data_dir, "config_example.json"), "Configuración JSON (1.4 KB)"),
        (os.path.join(sample_data_dir, "example_page.html"), "Página HTML (6.9 KB)"),
    ]
    
    for file_path, description in test_files:
        test_file(file_path, description)
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS".center(70))
    print("=" * 70)

if __name__ == "__main__":
    main()
