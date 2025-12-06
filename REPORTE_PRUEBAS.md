# Reporte de Pruebas - LZ78 Compressor

**Universidad Distrital Francisco José de Caldas**  
**Teoría de la Información - 2025-III**  
**Fecha:** 6 de diciembre de 2025

---

## ✅ Resumen Ejecutivo

**Estado del Proyecto:** COMPLETADO Y FUNCIONAL

**Total de Pruebas:** 6/6 EXITOSAS ✅

El programa LZ78 Compressor ha sido desarrollado completamente con arquitectura MVC y ha pasado todas las pruebas funcionales.

---

## 🧪 Pruebas Realizadas

### TEST 1: Compresión ✅
- **Estado:** EXITOSO
- **Descripción:** Compresión de archivo de texto usando algoritmo LZ78
- **Resultados:**
  - Archivo leído correctamente: `test_sample.txt` (618 caracteres)
  - Diccionario generado: 264 entradas
  - Datos comprimidos: 265 tuplas
  - Estadísticas calculadas correctamente

### TEST 2: Guardar y Cargar Archivos Comprimidos ✅
- **Estado:** EXITOSO
- **Descripción:** Guardar archivo .lz78 y recargarlo
- **Resultados:**
  - Archivo guardado correctamente en formato .lz78
  - Archivo cargado exitosamente
  - Integridad de datos verificada: datos cargados coinciden 100% con originales
  - Diccionario y datos comprimidos preservados

### TEST 3: Descompresión ✅
- **Estado:** EXITOSO
- **Descripción:** Descomprimir archivo .lz78 y reconstruir texto original
- **Resultados:**
  - Descompresión exitosa
  - Texto reconstruido: 618 caracteres
  - **VERIFICACIÓN CRÍTICA:** Texto descomprimido coincide PERFECTAMENTE con el original

### TEST 4: Guardar Archivo Descomprimido ✅
- **Estado:** EXITOSO
- **Descripción:** Guardar texto descomprimido en archivo .txt
- **Resultados:**
  - Archivo guardado correctamente
  - Verificación de contenido exitosa

### TEST 5: Manejo de Errores ✅
- **Estado:** EXITOSO
- **Descripción:** Validación de manejo de excepciones
- **Resultados:**
  - ✓ FileNotFoundError para archivos inexistentes
  - ✓ ValueError para archivos con formato incorrecto
  - ✓ ValueError para archivos vacíos
  - Todos los errores manejados correctamente

### TEST 6: Estructura del Diccionario ✅
- **Estado:** EXITOSO
- **Descripción:** Verificar correcta construcción del diccionario LZ78
- **Texto de prueba:** `'abababcabcd'`
- **Resultados:**
  ```
  Diccionario generado:
    1: 'a'
    2: 'b'
    3: 'ab'
    4: 'abc'
    5: 'abcd'
  
  Compresión: [(0,'a'), (0,'b'), (1,'b'), (3,'c'), (4,'d')]
  ```
- **Verificación:** Descompresión correcta del texto original

---

## 📊 Características Verificadas

### Funcionalidades Implementadas ✅

1. **Compresión de Archivos**
   - ✅ Lectura de archivos de texto
   - ✅ Algoritmo LZ78 implementado correctamente
   - ✅ Generación de diccionario
   - ✅ Producción de datos comprimidos

2. **Formato .lz78 Personalizado**
   - ✅ Guardado en formato JSON estructurado
   - ✅ Incluye: datos comprimidos, diccionario, nombre original
   - ✅ Versión del formato incluida

3. **Descompresión**
   - ✅ Carga de archivos .lz78
   - ✅ Reconstrucción exacta del texto original
   - ✅ Sin pérdida de datos

4. **Validaciones**
   - ✅ Validación de archivos vacíos
   - ✅ Validación de formatos incorrectos
   - ✅ Validación de archivos inexistentes
   - ✅ Manejo de errores de lectura/escritura

5. **Estadísticas**
   - ✅ Tamaño original calculado
   - ✅ Tamaño comprimido calculado
   - ✅ Ratio de compresión calculado
   - ✅ Tamaño del diccionario reportado

6. **Interfaz Gráfica (PyQt5)**
   - ✅ Aplicación GUI lanzada exitosamente
   - ✅ Interfaz moderna y profesional
   - ✅ Tres pestañas: Compresión, Descompresión, Diccionario
   - ✅ Botones de carga de archivos
   - ✅ Visualización de datos
   - ✅ Panel de estadísticas

7. **Arquitectura MVC**
   - ✅ Model: `lz78_compressor.py`, `file_handler.py`
   - ✅ View: `main_window.py`
   - ✅ Controller: `app_controller.py`
   - ✅ Separación de responsabilidades correcta

---

## 🎯 Requisitos del Proyecto Cumplidos

| Requisito | Estado | Notas |
|-----------|--------|-------|
| a) Capturar archivo de texto | ✅ | FileDialog implementado |
| b) Comprimir con LZ78 y mostrar diccionario | ✅ | Algoritmo completo + visualización |
| c) Guardar archivo .lz78 | ✅ | Formato JSON personalizado |
| d) Validar archivo no vacío y legible | ✅ | Validaciones implementadas |
| e) Cargar archivos .lz78 | ✅ | Función de carga completa |
| f) Descomprimir y visualizar diccionario | ✅ | Reconstrucción perfecta |
| g) Generar archivo con diccionario y mensaje | ✅ | Formato .lz78 incluye todo |
| h) Guardar archivo descomprimido | ✅ | Guardado de .txt |
| i) Mostrar estadísticas | ✅ | Panel completo de stats |
| j) Mensajes de error | ✅ | Diálogos de error/éxito |
| Arquitectura MVC | ✅ | Implementada correctamente |

---

## 🔍 Análisis de Compresión

**Nota Importante:** El ratio de compresión negativo (-362.22%) observado en las pruebas es **NORMAL** para textos pequeños con el algoritmo LZ78.

**Razón:**
- LZ78 necesita construir un diccionario desde cero
- Para textos pequeños, el overhead del diccionario es mayor que el texto original
- El algoritmo es eficiente con archivos grandes y repetitivos
- El formato JSON añade metadata adicional

**Solución:** LZ78 es óptimo para:
- Archivos grandes (>10KB)
- Textos con mucha repetición
- Documentos con patrones recurrentes

---

## 💻 Tecnologías Utilizadas

- **Lenguaje:** Python 3.13.3
- **GUI Framework:** PyQt5 5.15.9
- **Formato de datos:** JSON
- **Arquitectura:** MVC (Model-View-Controller)
- **Librerías estándar:** os, pathlib, json, typing

---

## 🚀 Estado de Deployment

✅ **Listo para Uso**

El programa está completamente funcional y listo para ser utilizado:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

---

## 📝 Conclusiones

1. ✅ Todos los requisitos del examen final están implementados
2. ✅ El algoritmo LZ78 funciona correctamente
3. ✅ La arquitectura MVC está bien estructurada
4. ✅ La interfaz gráfica es moderna y profesional
5. ✅ El manejo de errores es robusto
6. ✅ La integridad de datos está garantizada (descompresión perfecta)

**El proyecto está COMPLETO y FUNCIONAL.**

---

## 🎓 Puntos Adicionales Posibles

Para obtener puntos adicionales mencionados en el examen (comprimir otros formatos como Word, Excel), se podría implementar:

- Soporte para archivos binarios
- Compresión de múltiples archivos
- Análisis de patrones en diferentes tipos de archivos

**Estado actual:** El proyecto cumple todos los requisitos básicos del examen.

---

**Desarrollado por:** Julian Garcia  
**Institución:** Universidad Distrital Francisco José de Caldas  
**Materia:** Teoría de la Información 2025-III
