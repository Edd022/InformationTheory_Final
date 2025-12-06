# LZ78 File Compressor

**Universidad Distrital Francisco José de Caldas**  
Teoría de la Información - 2025-III

## Descripción

Aplicación con interfaz gráfica moderna para comprimir y descomprimir archivos de texto utilizando el algoritmo de compresión **LZ78**.

## Características

- ✅ Compresión de archivos de texto con algoritmo LZ78
- ✅ Descompresión de archivos .lz78
- ✅ Visualización del diccionario generado
- ✅ Estadísticas de compresión (tamaño original, comprimido, ratio)
- ✅ Interfaz gráfica moderna con PyQt5
- ✅ Arquitectura MVC (Model-View-Controller)
- ✅ Validación de archivos
- ✅ Manejo de errores completo

## Requisitos

- Python 3.10 o superior
- PyQt5 5.15.9 o superior

## Instalación

1. Clonar o descargar el repositorio:
```bash
git clone https://github.com/Edd022/InformationTheory_Final.git
cd InformationTheory_Final
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar la aplicación:
```bash
python main.py
```

### Operaciones Principales

1. **Comprimir un archivo:**
   - Click en "Load Text File"
   - Seleccionar archivo de texto
   - Click en "Compress"
   - Click en "Save Compressed File" para guardar

2. **Descomprimir un archivo:**
   - Click en "Load Compressed File (.lz78)"
   - Seleccionar archivo .lz78
   - Click en "Decompress"
   - Click en "Save Decompressed File" para guardar

3. **Ver el diccionario:**
   - Ir a la pestaña "Dictionary" para ver la estructura del diccionario LZ78

## Estructura del Proyecto

```
InformationTheory_Final/
├── src/
│   ├── model/
│   │   ├── __init__.py
│   │   ├── lz78_compressor.py    # Algoritmo LZ78
│   │   └── file_handler.py        # Manejo de archivos
│   ├── view/
│   │   ├── __init__.py
│   │   ├── main_window.py         # Interfaz principal
│   │   └── components/            # Componentes UI
│   ├── controller/
│   │   ├── __init__.py
│   │   └── app_controller.py      # Controlador MVC
│   └── utils/
│       └── __init__.py
├── resources/                      # Recursos (iconos, etc.)
├── tests/                         # Pruebas unitarias
├── docs/                          # Documentación
├── main.py                        # Punto de entrada
├── config.py                      # Configuración
├── requirements.txt               # Dependencias
└── README.md

```

## Arquitectura MVC

- **Model**: Lógica de negocio (algoritmo LZ78, manejo de archivos)
- **View**: Interfaz gráfica PyQt5
- **Controller**: Coordina Model y View

## Algoritmo LZ78

El algoritmo LZ78 comprime datos construyendo un diccionario de frases vistas previamente:

1. Lee la entrada carácter por carácter
2. Busca la frase más larga que ya existe en el diccionario
3. Emite un par (índice, siguiente_carácter)
4. Agrega la nueva frase al diccionario

## Formato de Archivo .lz78

Los archivos comprimidos se guardan en formato JSON:
```json
{
  "original_filename": "archivo.txt",
  "compressed_data": [[0, "a"], [1, "b"], ...],
  "dictionary": {"a": 1, "ab": 2, ...},
  "version": "1.0"
}
```

## Autores

- Julian Garcia
- Universidad Distrital Francisco José de Caldas

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
