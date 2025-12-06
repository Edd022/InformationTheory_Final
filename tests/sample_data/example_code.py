"""
Ejemplo de código Python con alta redundancia
Este archivo demuestra compresión efectiva en código fuente
"""

import os
import sys
import json
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Usuario:
    """Clase que representa un usuario del sistema."""
    id: int
    nombre: str
    email: str
    activo: bool = True
    
    def to_dict(self) -> Dict:
        """Convierte el usuario a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Usuario':
        """Crea un usuario desde un diccionario."""
        return cls(
            id=data['id'],
            nombre=data['nombre'],
            email=data['email'],
            activo=data.get('activo', True)
        )


class BaseDatosUsuarios:
    """Gestor de base de datos de usuarios."""
    
    def __init__(self, archivo_path: str):
        """Inicializa el gestor de base de datos."""
        self.archivo_path = archivo_path
        self.usuarios: List[Usuario] = []
        logger.info(f"Inicializando base de datos en {archivo_path}")
    
    def cargar_usuarios(self) -> bool:
        """Carga los usuarios desde el archivo JSON."""
        try:
            if not os.path.exists(self.archivo_path):
                logger.warning(f"Archivo {self.archivo_path} no existe")
                return False
            
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            self.usuarios = [Usuario.from_dict(u) for u in datos]
            logger.info(f"Cargados {len(self.usuarios)} usuarios")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando usuarios: {str(e)}")
            return False
    
    def guardar_usuarios(self) -> bool:
        """Guarda los usuarios en el archivo JSON."""
        try:
            datos = [u.to_dict() for u in self.usuarios]
            
            with open(self.archivo_path, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Guardados {len(self.usuarios)} usuarios")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando usuarios: {str(e)}")
            return False
    
    def agregar_usuario(self, usuario: Usuario) -> bool:
        """Agrega un nuevo usuario a la base de datos."""
        if self.buscar_usuario_por_id(usuario.id):
            logger.warning(f"Usuario con ID {usuario.id} ya existe")
            return False
        
        self.usuarios.append(usuario)
        logger.info(f"Usuario {usuario.nombre} agregado exitosamente")
        return True
    
    def buscar_usuario_por_id(self, id: int) -> Optional[Usuario]:
        """Busca un usuario por su ID."""
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None
    
    def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por su email."""
        for usuario in self.usuarios:
            if usuario.email == email:
                return usuario
        return None
    
    def actualizar_usuario(self, id: int, datos: Dict) -> bool:
        """Actualiza los datos de un usuario."""
        usuario = self.buscar_usuario_por_id(id)
        if not usuario:
            logger.warning(f"Usuario con ID {id} no encontrado")
            return False
        
        if 'nombre' in datos:
            usuario.nombre = datos['nombre']
        if 'email' in datos:
            usuario.email = datos['email']
        if 'activo' in datos:
            usuario.activo = datos['activo']
        
        logger.info(f"Usuario {id} actualizado exitosamente")
        return True
    
    def eliminar_usuario(self, id: int) -> bool:
        """Elimina un usuario de la base de datos."""
        usuario = self.buscar_usuario_por_id(id)
        if not usuario:
            logger.warning(f"Usuario con ID {id} no encontrado")
            return False
        
        self.usuarios.remove(usuario)
        logger.info(f"Usuario {id} eliminado exitosamente")
        return True
    
    def listar_usuarios_activos(self) -> List[Usuario]:
        """Retorna lista de usuarios activos."""
        return [u for u in self.usuarios if u.activo]
    
    def listar_usuarios_inactivos(self) -> List[Usuario]:
        """Retorna lista de usuarios inactivos."""
        return [u for u in self.usuarios if not u.activo]
    
    def contar_usuarios(self) -> int:
        """Retorna el número total de usuarios."""
        return len(self.usuarios)
    
    def contar_usuarios_activos(self) -> int:
        """Retorna el número de usuarios activos."""
        return len(self.listar_usuarios_activos())
    
    def contar_usuarios_inactivos(self) -> int:
        """Retorna el número de usuarios inactivos."""
        return len(self.listar_usuarios_inactivos())


def main():
    """Función principal del programa."""
    logger.info("Iniciando aplicación de gestión de usuarios")
    
    # Crear instancia de la base de datos
    db = BaseDatosUsuarios('usuarios.json')
    
    # Cargar usuarios existentes
    if not db.cargar_usuarios():
        logger.info("Creando nueva base de datos")
    
    # Agregar usuarios de ejemplo
    usuarios_ejemplo = [
        Usuario(id=1, nombre="Juan Pérez", email="juan@example.com"),
        Usuario(id=2, nombre="María García", email="maria@example.com"),
        Usuario(id=3, nombre="Carlos López", email="carlos@example.com"),
        Usuario(id=4, nombre="Ana Martínez", email="ana@example.com"),
        Usuario(id=5, nombre="Pedro Rodríguez", email="pedro@example.com"),
    ]
    
    for usuario in usuarios_ejemplo:
        db.agregar_usuario(usuario)
    
    # Guardar cambios
    db.guardar_usuarios()
    
    # Mostrar estadísticas
    logger.info(f"Total de usuarios: {db.contar_usuarios()}")
    logger.info(f"Usuarios activos: {db.contar_usuarios_activos()}")
    logger.info(f"Usuarios inactivos: {db.contar_usuarios_inactivos()}")
    
    logger.info("Aplicación finalizada exitosamente")


if __name__ == "__main__":
    main()
