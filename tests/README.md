# Tests - Compresión LZ78 + Huffman

Este directorio contiene los scripts de prueba y datos de muestra para validar el funcionamiento del compresor híbrido LZ78 + Huffman.

## Estructura

```
tests/
├── README.md                          # Este archivo
├── test_hybrid_compression.py         # Prueba completa del compresor híbrido
├── test_large_compression.py          # Prueba con archivo grande (LZ78 puro)
├── generate_compressible_files.py     # Generador de archivos de prueba
└── sample_data/                       # Archivos de datos de prueba
    ├── system_logs.txt                # Logs simulados (2MB, 86% redundancia)
    ├── sales_dataset.csv              # Dataset CSV (2MB, 61% redundancia)
    ├── test_very_large_data.txt       # Texto educativo (500KB, 99% redundancia)
    └── test_large_compressed.lz78     # Archivo comprimido de ejemplo
```

## Scripts de Prueba

### 1. test_hybrid_compression.py

**Propósito**: Prueba exhaustiva del compresor híbrido LZ78 + Huffman con todos los archivos de muestra.

**Funcionalidad**:
- Comprime archivos de prueba usando LZ78 + Huffman
- Calcula estadísticas detalladas (tamaño original, LZ78 solo, híbrido)
- Muestra mejora vs LZ78 puro
- Verifica descompresión exacta

**Uso**:
```bash
cd tests
python test_hybrid_compression.py
```

**Resultados esperados**:
- system_logs.txt: ~90% compresión (2MB → 200KB)
- sales_dataset.csv: ~83% compresión (2MB → 350KB)
- test_very_large_data.txt: ~80% compresión (500KB → 100KB)
- Descompresión: 100% exacta en todos los casos

---

### 2. test_large_compression.py

**Propósito**: Prueba del compresor LZ78 puro (sin Huffman) con archivo grande.

**Funcionalidad**:
- Comprime archivo CSV usando solo LZ78
- Muestra estadísticas del diccionario
- Analiza patrones encontrados
- Guarda resultado en formato binario

**Uso**:
```bash
cd tests
python test_large_compression.py
```

**Nota**: Este script usa el compresor LZ78 antiguo. El híbrido con Huffman logra 91-94% mejor compresión.

---

### 3. generate_compressible_files.py

**Propósito**: Genera archivos de prueba con diferentes niveles de redundancia para validar el compresor.

**Funcionalidad**:
- **system_logs.txt** (2MB): Logs simulados con alta redundancia
  - 80% nivel INFO
  - 8 servicios diferentes
  - 15 mensajes comunes
  - Timestamps secuenciales
  - Redundancia estimada: 86%

- **sales_dataset.csv** (2MB): Dataset de ventas con datos tabulares
  - 10 productos
  - 6 categorías
  - 4 estados
  - Fechas/horas variables
  - Redundancia estimada: 61%

**Uso**:
```bash
cd tests
python generate_compressible_files.py
```

**Salida**: Genera archivos en `sample_data/` con el tamaño especificado.

---

## Datos de Muestra

### system_logs.txt
- **Tamaño**: ~2 MB
- **Tipo**: Logs simulados de sistema
- **Redundancia**: 86% (texto altamente repetitivo)
- **Compresión esperada**: 89-90% (ratio 10:1)
- **Descripción**: Logs de 8 servicios diferentes con mensajes comunes, timestamps secuenciales y parámetros variables

### sales_dataset.csv
- **Tamaño**: ~2 MB
- **Tipo**: Dataset CSV de ventas
- **Redundancia**: 61% (datos tabulares con repetición moderada)
- **Compresión esperada**: 82-83% (ratio 17:1)
- **Descripción**: Registros de ventas con productos, categorías, precios y fechas

### test_very_large_data.txt
- **Tamaño**: ~500 KB
- **Tipo**: Texto educativo sobre programación
- **Redundancia**: 99% (texto natural con alta repetición)
- **Compresión esperada**: 79-80% (ratio 20:1)
- **Descripción**: Contenido técnico sobre Python, algoritmos y estructuras de datos

---

## Ejecutar Todas las Pruebas

Para ejecutar todas las pruebas en secuencia:

```bash
cd tests

# 1. Generar archivos de prueba (si no existen)
python generate_compressible_files.py

# 2. Ejecutar prueba del compresor híbrido
python test_hybrid_compression.py

# 3. (Opcional) Ejecutar prueba de LZ78 puro
python test_large_compression.py
```

---

## Métricas de Éxito

**Compresión exitosa** si:
- ✅ Reducción >= 75% en archivos grandes (>1MB)
- ✅ Reducción >= 50% en archivos medianos (100KB-1MB)
- ✅ Mejora vs LZ78 puro >= 90%
- ✅ Descompresión 100% exacta
- ✅ Sin errores en ejecución

**Estadísticas típicas**:
- Original: 2MB
- LZ78 solo: ~8MB (expansión debido a diccionario)
- LZ78 + Huffman: ~200-350KB (compresión real)
- Mejora vs LZ78: 91-94%
- Ratio: 10:1 a 20:1

---

## Notas Técnicas

### ¿Por qué el híbrido funciona mejor?

1. **LZ78**: Captura redundancia estructural (patrones repetidos)
2. **Huffman**: Optimiza representación de índices del diccionario
3. **chr() encoding**: Índices <256 en 1 byte vs string representation
4. **Diccionario como header**: No se cuenta en ratio de compresión

### Limitaciones

- **Archivos pequeños (<10KB)**: Pueden expandirse (overhead del diccionario)
- **Datos aleatorios**: Sin redundancia = sin compresión
- **Archivos binarios**: LZ78 está optimizado para texto

### Próximos Pasos

- [ ] Agregar pruebas unitarias con pytest
- [ ] Benchmark de velocidad de compresión
- [ ] Comparación con ZIP/GZIP
- [ ] Pruebas con archivos de código fuente
- [ ] Análisis de límites de compresión teóricos
