"""
Script de prueba para archivo grande (>100KB) con el algoritmo LZ78
Verifica si la implementación logra compresión efectiva en archivos grandes
"""

import sys
import os

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model.lz78_compressor import LZ78Compressor
from model.file_handler_binary import FileHandlerBinary

def format_bytes(bytes_size):
    """Formatear bytes en unidades legibles"""
    for unit in ['bytes', 'KB', 'MB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:>7.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} GB"

def main():
    print("=" * 80)
    print("PRUEBA DE COMPRESIÓN LZ78 CON ARCHIVO GRANDE (>100KB)".center(80))
    print("=" * 80)
    print()
    
    # Nombre del archivo a probar
    test_file = "test_very_large_data.txt"
    
    if not os.path.exists(test_file):
        print(f"❌ Error: No se encontró el archivo {test_file}")
        return
    
    # Leer archivo
    print(f"📂 Leyendo archivo: {test_file}")
    file_handler = FileHandlerBinary()
    with open(test_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    original_size = len(text.encode('utf-8'))
    num_chars = len(text)
    num_words = len(text.split())
    num_lines = text.count('\n') + 1
    
    print(f"   Tamaño: {format_bytes(original_size)}")
    print(f"   Caracteres: {num_chars:,}")
    print(f"   Palabras: {num_words:,}")
    print(f"   Líneas: {num_lines:,}")
    print()
    
    # Comprimir
    print("⚙️  Comprimiendo con LZ78...")
    compressor = LZ78Compressor()
    compressed_data, dictionary = compressor.compress(text)
    
    print(f"   ✓ Compresión completada")
    print(f"   Entradas en diccionario: {len(dictionary):,}")
    print(f"   Tuplas comprimidas: {len(compressed_data):,}")
    print()
    
    # Calcular tamaño comprimido
    compressed_size = file_handler.get_compressed_size(compressed_data, dictionary, test_file)
    
    # Calcular métricas
    if compressed_size < original_size:
        reduction = original_size - compressed_size
        percentage = (reduction / original_size) * 100
        ratio = compressed_size / original_size
        print("📊 RESULTADOS:")
        print(f"   Tamaño original:       {format_bytes(original_size)}")
        print(f"   Tamaño comprimido:     {format_bytes(compressed_size)}")
        print(f"   Reducción:             {format_bytes(reduction)}")
        print(f"   ✅ COMPRESIÓN EXITOSA: {percentage:.2f}% de reducción")
        print(f"   Razón de compresión:   {ratio:.2f}:1")
    else:
        increase = compressed_size - original_size
        percentage = (increase / original_size) * 100
        ratio = compressed_size / original_size
        print("📊 RESULTADOS:")
        print(f"   Tamaño original:       {format_bytes(original_size)}")
        print(f"   Tamaño comprimido:     {format_bytes(compressed_size)}")
        print(f"   Aumento:               {format_bytes(increase)}")
        print(f"   ⚠️  EXPANSIÓN: {percentage:.2f}% de aumento")
        print(f"   Factor: {ratio:.2f}:1")
    print()
    
    # Verificar descompresión
    print("🔄 Verificando descompresión...")
    decompressed = compressor.decompress(compressed_data, dictionary)
    
    if decompressed == text:
        print("   ✅ Descompresión correcta - texto idéntico al original")
    else:
        print("   ❌ Error: El texto descomprimido no coincide con el original")
        return
    print()
    
    # Guardar archivo comprimido
    output_file = "test_large_compressed.lz78"
    print(f"💾 Guardando archivo comprimido: {output_file}")
    file_handler.save_compressed_file(output_file, compressed_data, dictionary, test_file)
    
    actual_size = os.path.getsize(output_file)
    print(f"   ✓ Archivo guardado")
    print(f"   Tamaño real del archivo: {format_bytes(actual_size)}")
    
    if abs(actual_size - compressed_size) < 10:
        print(f"   ✓ Tamaño coincide con el cálculo")
    else:
        print(f"   ⚠️  Discrepancia: calculado={compressed_size}, real={actual_size}")
    print()
    
    # Análisis de patrones
    print("=" * 80)
    print("📈 ANÁLISIS DE PATRONES:")
    print()
    
    # Contar palabras más frecuentes
    words = text.lower().split()
    word_freq = {}
    for word in words:
        # Limpiar puntuación
        word = ''.join(c for c in word if c.isalnum() or c in 'áéíóúñü')
        if word:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Top 10 palabras
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    print("   Top 10 palabras más frecuentes:")
    for word, count in sorted_words:
        print(f"      '{word}': {count} veces")
    
    unique_words = len(word_freq)
    total_words = len(words)
    redundancy = ((total_words - unique_words) / total_words) * 100
    
    print()
    print(f"   Palabras únicas: {unique_words:,}")
    print(f"   Palabras totales: {total_words:,}")
    print(f"   Redundancia: {redundancy:.2f}%")
    print()
    
    # Conclusión
    print("=" * 80)
    print("CONCLUSIÓN:")
    print("=" * 80)
    
    if compressed_size < original_size:
        print("✅ El algoritmo LZ78 logró COMPRIMIR el archivo exitosamente.")
        print(f"   El archivo grande ({format_bytes(original_size).strip()}) se redujo en {percentage:.2f}%.")
        print("   La implementación está funcionando correctamente.")
    else:
        print("⚠️  El archivo resultó más grande después de la compresión.")
        print(f"   Esto puede deberse a que el archivo ({format_bytes(original_size).strip()})")
        print("   aún no es lo suficientemente grande para que LZ78 sea efectivo.")
        print(f"   El diccionario ({len(dictionary):,} entradas) añade overhead significativo.")
        print()
        print("   Nota: LZ78 generalmente necesita archivos >100-200 KB con alta")
        print("   redundancia para lograr compresión neta positiva.")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
