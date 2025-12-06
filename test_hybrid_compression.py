"""
Script de prueba para compresión híbrida LZ78 + Huffman
Verifica la mejora vs LZ78 puro
"""

import sys
import os

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model.lz78_huffman_compressor import LZ78HuffmanCompressor
from model.file_handler_binary_huffman import FileHandlerBinaryHuffman

def format_bytes(bytes_size):
    """Formatear bytes en unidades legibles"""
    if bytes_size < 1024:
        return f"{bytes_size:>7} bytes"
    elif bytes_size < 1024*1024:
        return f"{bytes_size/1024:>7.2f} KB"
    else:
        return f"{bytes_size/(1024*1024):>7.2f} MB"

def main():
    print("=" * 80)
    print("PRUEBA DE COMPRESIÓN HÍBRIDA LZ78 + HUFFMAN".center(80))
    print("=" * 80)
    print()
    
    # Archivos de prueba
    test_files = [
        ("system_logs.txt", "Logs del sistema (2MB, alta redundancia)"),
        ("sales_dataset.csv", "Dataset CSV (2MB, datos tabulares)"),
        ("test_very_large_data.txt", "Texto educativo (500KB)")
    ]
    
    for test_file, description in test_files:
        if not os.path.exists(test_file):
            print(f"⚠️  Saltando {test_file} (no encontrado)")
            print()
            continue
        
        print(f"📂 Probando: {test_file}")
        print(f"   Descripción: {description}")
        print()
        
        # Leer archivo
        with open(test_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        original_size = len(text.encode('utf-8'))
        print(f"   📊 Tamaño original: {format_bytes(original_size)}")
        
        # Comprimir con LZ78 + Huffman
        print(f"   ⚙️  Comprimiendo con LZ78 + Huffman...")
        compressor = LZ78HuffmanCompressor()
        compressed_data, lz78_dict, huffman_codes, encoded_indices = compressor.compress(text)
        
        # Calcular estadísticas
        stats = compressor.get_statistics(
            text, test_file,
            compressed_data, lz78_dict,
            huffman_codes, encoded_indices
        )
        
        print(f"   ✓ Compresión completada")
        print()
        print(f"   📈 RESULTADOS:")
        print(f"      Tamaño original:     {format_bytes(stats['original_size'])}")
        print(f"      LZ78 solo:           {format_bytes(stats['lz78_only_size'])}")
        print(f"      LZ78 + Huffman:      {format_bytes(stats['hybrid_size'])}")
        print()
        
        if stats['hybrid_size'] < stats['original_size']:
            reduction = stats['original_size'] - stats['hybrid_size']
            percentage = (reduction / stats['original_size']) * 100
            print(f"      ✅ COMPRESIÓN EXITOSA!")
            print(f"         Reducción: {format_bytes(reduction)} ({percentage:.2f}%)")
            print(f"         Ratio: {stats['compression_ratio']:.2f}:1")
        else:
            increase = stats['hybrid_size'] - stats['original_size']
            percentage = (increase / stats['original_size']) * 100
            print(f"      ⚠️  EXPANSIÓN: {format_bytes(increase)} ({percentage:.2f}%)")
        
        print()
        print(f"      🔧 Mejora vs LZ78 puro: {stats['improvement_vs_lz78']:.2f}%")
        print(f"      📚 Entradas en diccionario: {stats['dictionary_entries']:,}")
        print(f"      🔤 Códigos Huffman: {stats['huffman_codes_count']}")
        print(f"      📡 Bits Huffman: {stats['huffman_bits']:,} ({stats['huffman_bytes']:,} bytes)")
        print()
        
        # Verificar descompresión
        print(f"   🔄 Verificando descompresión...")
        decompressed = compressor.decompress(
            compressed_data, lz78_dict,
            huffman_codes, encoded_indices
        )
        
        if decompressed == text:
            print(f"      ✅ Descompresión perfecta (100% exacta)")
        else:
            print(f"      ❌ ERROR: Descompresión incorrecta")
        
        print()
        print("   " + "-" * 74)
        print()
    
    print("=" * 80)
    print("PRUEBAS COMPLETADAS".center(80))
    print("=" * 80)

if __name__ == "__main__":
    main()
