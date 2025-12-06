# LZ78 File Compressor

**Universidad Distrital Francisco José de Caldas**  
Teoría de la Información - 2025-III

## Descripción

Aplicación con interfaz gráfica para comprimir y descomprimir archivos de texto utilizando el algoritmo LZ78. Desarrollada en Python con arquitectura MVC y PyQt5.

## Características

- Compresión y descompresión de archivos de texto con algoritmo LZ78
- Formato personalizado .lz78 para archivos comprimidos
- Visualización del diccionario generado durante la compresión
- Estadísticas detalladas (tamaño original, comprimido, ratio de compresión)
- Interfaz gráfica moderna en español
- Validación completa de archivos y manejo de errores
- Arquitectura MVC (Model-View-Controller)

## Nota Importante sobre LZ78

El algoritmo LZ78 construye un diccionario dinámico durante la compresión. Para archivos pequeños o medianos (menores a 10KB), el tamaño del archivo comprimido puede ser **mayor** que el original debido a:

1. **Overhead del diccionario**: LZ78 debe almacenar todas las entradas del diccionario junto con los datos comprimidos
2. **Formato de almacenamiento**: El archivo .lz78 incluye metadatos y estructura JSON
3. **Tamaño del archivo**: Textos pequeños no tienen suficiente repetición para amortizar el overhead

**LZ78 es más eficiente con:**
- Archivos grandes (mayores a 10KB)
- Textos con alta repetición de patrones
- Documentos con vocabulario limitado

Para archivos pequeños, el ratio de compresión será negativo (expansión), lo cual es el comportamiento esperado del algoritmo.

## Requisitos

- Python 3.10 o superior
- PyQt5 5.15.9 o superior

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Edd022/InformationTheory_Final.git
cd InformationTheory_Final
```

2. Crear entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar la aplicación:
```bash
python main.py
```

### Comprimir un archivo

1. Click en "Cargar Archivo de Texto"
2. Seleccionar archivo .txt
3. Click en "Comprimir"
4. Click en "Guardar Archivo Comprimido" para guardar el .lz78

### Descomprimir un archivo

1. Click en "Cargar Archivo Comprimido (.lz78)"
2. Seleccionar archivo .lz78
3. Click en "Descomprimir"
4. Click en "Guardar Archivo Descomprimido" para exportar

### Visualizar diccionario

Navegar a la pestaña "Diccionario" para ver la estructura interna del algoritmo LZ78.

## Estructura del Proyecto

```
InformationTheory_Final/
├── src/
│   ├── model/
│   │   ├── lz78_compressor.py    # Algoritmo LZ78
│   │   └── file_handler.py        # Manejo de archivos
│   ├── view/
│   │   ├── main_window.py         # Interfaz PyQt5
│   │   └── components/            # Componentes UI
│   ├── controller/
│   │   └── app_controller.py      # Controlador MVC
│   └── utils/
├── resources/                      # Recursos
├── tests/                         # Pruebas
├── docs/                          # Documentación
├── main.py                        # Punto de entrada
├── config.py                      # Configuración
└── requirements.txt               # Dependencias
```

## Arquitectura

El proyecto implementa el patrón MVC:

- **Model**: Lógica de negocio (algoritmo LZ78, operaciones de archivos)
- **View**: Interfaz gráfica con PyQt5
- **Controller**: Coordinación entre Model y View

## Algoritmo LZ78

LZ78 comprime datos mediante construcción dinámica de diccionario:

1. Lee la entrada carácter por carácter
2. Busca la frase más larga que existe en el diccionario
3. Emite un par (índice_diccionario, siguiente_carácter)
4. Agrega la nueva frase al diccionario
5. Repite hasta procesar toda la entrada

Durante la descompresión, se reconstruye el texto usando el diccionario guardado y las tuplas de datos comprimidos.

## Formato .lz78

Los archivos comprimidos se guardan en formato JSON optimizado:

```json
{"original_filename":"archivo.txt","compressed_data":[[0,"a"],[1,"b"]],"dictionary":{"a":1,"ab":2},"version":"1.0"}
```

El formato incluye:
- `original_filename`: Nombre del archivo original
- `compressed_data`: Lista de tuplas (índice, carácter)
- `dictionary`: Diccionario de compresión
- `version`: Versión del formato

## Pruebas

Ejecutar suite de pruebas:
```bash
python test_program.py
```

Las pruebas verifican:
- Compresión y descompresión
- Integridad de datos
- Guardado y carga de archivos
- Manejo de errores
- Estructura del diccionario

## Limitaciones Conocidas

1. **Tamaño de archivos pequeños**: Como se mencionó, LZ78 no es eficiente para textos menores a 10KB
2. **Solo archivos de texto**: La versión actual solo soporta archivos de texto plano
3. **Formato JSON**: Aunque optimizado, JSON añade overhead adicional comparado con formatos binarios

## Posibles Mejoras Futuras

- Implementar formato binario para reducir overhead
- Soporte para archivos binarios (Word, Excel, PDF)
- Compresión de múltiples archivos
- Implementación de LZW para mejor ratio de compresión
- Modo de compresión configurable

## Autor

Julian Garcia  
Universidad Distrital Francisco José de Caldas  
Teoría de la Información 2025-III

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.
