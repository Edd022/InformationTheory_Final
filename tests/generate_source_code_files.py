"""
Generador de archivos de código fuente grandes para pruebas de compresión
Crea archivos con alta redundancia típica de código fuente
"""

import random
import os

def generate_large_python_file(filename="large_code.py", size_kb=50):
    """Genera un archivo Python grande con código repetitivo"""
    
    print(f"Generando archivo Python de ~{size_kb} KB...")
    
    # Directorio de salida
    output_dir = os.path.join(os.path.dirname(__file__), 'sample_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    # Nombres comunes en código
    class_names = ["User", "Product", "Order", "Customer", "Payment", "Invoice", "Report", "Database", "Service", "Manager"]
    method_names = ["get", "set", "create", "update", "delete", "find", "list", "save", "load", "validate"]
    var_names = ["data", "result", "value", "item", "obj", "instance", "response", "request", "config", "params"]
    
    target_bytes = size_kb * 1024
    current_bytes = 0
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        header = '''"""
Archivo de código Python generado automáticamente
Demuestra compresión en archivos de código fuente con patrones repetitivos
"""

import os
import sys
import json
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


'''
        f.write(header)
        current_bytes += len(header.encode('utf-8'))
        
        # Generar clases
        class_counter = 1
        while current_bytes < target_bytes:
            class_name = random.choice(class_names) + str(class_counter)
            
            class_code = f'''
@dataclass
class {class_name}:
    """Clase {class_name} del sistema."""
    id: int
    name: str
    description: str
    active: bool = True
    created_at: str = ""
    updated_at: str = ""
    
    def __init__(self, id: int, name: str, description: str):
        """Inicializa una instancia de {class_name}."""
        self.id = id
        self.name = name
        self.description = description
        self.active = True
        logger.info(f"Creado {class_name} con ID {{self.id}}")
    
    def to_dict(self) -> Dict:
        """Convierte {class_name} a diccionario."""
        return {{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }}
    
    @classmethod
    def from_dict(cls, data: Dict) -> '{class_name}':
        """Crea {class_name} desde diccionario."""
        instance = cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', '')
        )
        instance.active = data.get('active', True)
        instance.created_at = data.get('created_at', '')
        instance.updated_at = data.get('updated_at', '')
        return instance
    
    def validate(self) -> bool:
        """Valida los datos de {class_name}."""
        if not self.id or self.id < 0:
            logger.error(f"ID inválido en {class_name}: {{self.id}}")
            return False
        if not self.name or len(self.name) == 0:
            logger.error(f"Nombre inválido en {class_name}")
            return False
        logger.info(f"{class_name} validado correctamente")
        return True
    
    def save_to_file(self, filename: str) -> bool:
        """Guarda {class_name} en archivo JSON."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4)
            logger.info(f"{class_name} guardado en {{filename}}")
            return True
        except Exception as e:
            logger.error(f"Error guardando {class_name}: {{str(e)}}")
            return False
    
    @classmethod
    def load_from_file(cls, filename: str) -> Optional['{class_name}']:
        """Carga {class_name} desde archivo JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"{class_name} cargado desde {{filename}}")
            return cls.from_dict(data)
        except Exception as e:
            logger.error(f"Error cargando {class_name}: {{str(e)}}")
            return None


'''
            f.write(class_code)
            current_bytes += len(class_code.encode('utf-8'))
            class_counter += 1
            
            # Agregar funciones de utilidad cada 3 clases
            if class_counter % 3 == 0:
                method = random.choice(method_names)
                var = random.choice(var_names)
                util_code = f'''
def {method}_{var}(id: int, {var}: Dict) -> bool:
    """Función de utilidad para {method} {var}."""
    try:
        logger.info(f"Ejecutando {method}_{var} con ID {{id}}")
        if not {var}:
            logger.warning(f"{var} vacío en {method}_{var}")
            return False
        logger.info(f"{method}_{var} completado exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error en {method}_{var}: {{str(e)}}")
        return False


'''
                f.write(util_code)
                current_bytes += len(util_code.encode('utf-8'))
        
        # Main function
        main_code = '''
def main():
    """Función principal del sistema."""
    logger.info("Iniciando aplicación")
    logger.info("Aplicación finalizada")


if __name__ == "__main__":
    main()
'''
        f.write(main_code)
        current_bytes += len(main_code.encode('utf-8'))
    
    actual_size = current_bytes / 1024
    print(f"Archivo generado: {filename} ({actual_size:.2f} KB)")
    return current_bytes


def main():
    """Genera archivos de código fuente para pruebas."""
    print("=" * 70)
    print("GENERADOR DE ARCHIVOS DE CÓDIGO FUENTE".center(70))
    print("=" * 70)
    print()
    
    # Generar archivo Python de 50KB
    generate_large_python_file("large_code.py", size_kb=50)
    
    print()
    print("=" * 70)
    print("GENERACIÓN COMPLETADA".center(70))
    print("=" * 70)


if __name__ == "__main__":
    main()
