"""
Generador de archivos altamente comprimibles para probar LZ78
Genera logs y CSV con alta redundancia para demostrar compresión efectiva
"""

import random
from datetime import datetime, timedelta

def generate_system_logs(filename="system_logs.txt", size_mb=2):
    """Genera archivo de logs simulados con alta redundancia"""
    
    print(f"Generando logs simulados de ~{size_mb} MB...")
    
    # Componentes altamente repetitivos de logs
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    services = [
        "AuthService", "DatabaseService", "CacheService", "APIGateway",
        "UserManager", "FileHandler", "NetworkMonitor", "SystemScheduler"
    ]
    
    messages = [
        "Proceso completado exitosamente",
        "Conexión establecida correctamente",
        "Solicitud procesada en {} ms",
        "Recurso liberado correctamente",
        "Cache actualizado exitosamente",
        "Sesión iniciada para usuario {}",
        "Query ejecutado en {} ms",
        "Memoria utilizada: {}%",
        "CPU utilizada: {}%",
        "Disco disponible: {} GB",
        "Conexiones activas: {}",
        "Operación completada sin errores",
        "Archivo procesado correctamente",
        "Token de autenticación validado",
        "Datos sincronizados con éxito"
    ]
    
    error_messages = [
        "Error al conectar con la base de datos",
        "Timeout esperando respuesta del servidor",
        "Permiso denegado para operación",
        "Recurso no encontrado: {}",
        "Fallo en autenticación de usuario",
        "Error al procesar solicitud"
    ]
    
    users = ["admin", "user001", "user002", "system", "service_account"]
    
    # Generar logs
    start_date = datetime(2024, 12, 1, 0, 0, 0)
    current_date = start_date
    
    target_bytes = size_mb * 1024 * 1024
    current_bytes = 0
    
    with open(filename, 'w', encoding='utf-8') as f:
        while current_bytes < target_bytes:
            # Incrementar tiempo
            current_date += timedelta(seconds=random.randint(1, 5))
            timestamp = current_date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            # Seleccionar nivel de log (80% INFO, resto distribuido)
            if random.random() < 0.8:
                level = "INFO"
                message = random.choice(messages)
                service = random.choice(services)
            elif random.random() < 0.9:
                level = "WARNING"
                message = random.choice(messages)
                service = random.choice(services)
            else:
                level = "ERROR"
                message = random.choice(error_messages)
                service = random.choice(services)
            
            # Formatear mensaje con parámetros
            if "{}" in message:
                if "ms" in message:
                    param = random.randint(10, 500)
                elif "%" in message:
                    param = random.randint(30, 95)
                elif "GB" in message:
                    param = random.randint(100, 900)
                elif "usuario" in message:
                    param = random.choice(users)
                elif "Recurso" in message:
                    param = f"/api/v1/resource/{random.randint(1, 100)}"
                else:
                    param = random.randint(1, 100)
                message = message.format(param)
            
            # Escribir línea de log
            log_line = f"[{timestamp}] {level:8} [{service}] {message}\n"
            f.write(log_line)
            current_bytes += len(log_line.encode('utf-8'))
            
            # Cada 1000 líneas, agregar separador
            if random.randint(1, 1000) == 1:
                separator = f"\n{'='*80}\n"
                f.write(separator)
                current_bytes += len(separator.encode('utf-8'))
    
    actual_size = current_bytes / (1024 * 1024)
    print(f"✓ {filename} generado: {actual_size:.2f} MB")
    return current_bytes


def generate_csv_dataset(filename="dataset.csv", size_mb=2):
    """Genera dataset CSV con datos repetitivos"""
    
    print(f"Generando dataset CSV de ~{size_mb} MB...")
    
    # Datos con alta redundancia
    productos = [
        "Laptop Dell Inspiron 15", "Mouse Logitech MX Master",
        "Teclado Mecánico Corsair", "Monitor Samsung 27\"",
        "Webcam Logitech C920", "Audífonos Sony WH-1000XM4",
        "Disco SSD Kingston 500GB", "Memoria RAM Crucial 16GB",
        "Router TP-Link AC1750", "Hub USB-C Anker 7 puertos"
    ]
    
    categorias = [
        "Computadoras", "Accesorios", "Periféricos", 
        "Audio", "Almacenamiento", "Redes"
    ]
    
    estados = ["Activo", "En Stock", "Agotado", "En Pedido"]
    sucursales = ["Sucursal Centro", "Sucursal Norte", "Sucursal Sur", "Almacén Central"]
    
    target_bytes = size_mb * 1024 * 1024
    current_bytes = 0
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Encabezado
        header = "ID,Fecha,Hora,Producto,Categoría,Cantidad,Precio_Unitario,Total,Estado,Sucursal,Vendedor\n"
        f.write(header)
        current_bytes += len(header.encode('utf-8'))
        
        # Generar registros
        id_counter = 1
        base_date = datetime(2024, 1, 1)
        
        while current_bytes < target_bytes:
            # Datos del registro
            date_offset = random.randint(0, 365)
            fecha = (base_date + timedelta(days=date_offset)).strftime("%Y-%m-%d")
            hora = f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
            
            producto = random.choice(productos)
            categoria = random.choice(categorias)
            cantidad = random.randint(1, 100)
            precio = round(random.uniform(10.0, 1500.0), 2)
            total = round(cantidad * precio, 2)
            estado = random.choice(estados)
            sucursal = random.choice(sucursales)
            vendedor = f"VEN{random.randint(1, 20):03d}"
            
            # Escribir línea
            row = f"{id_counter:06d},{fecha},{hora},{producto},{categoria},{cantidad},{precio:.2f},{total:.2f},{estado},{sucursal},{vendedor}\n"
            f.write(row)
            current_bytes += len(row.encode('utf-8'))
            id_counter += 1
    
    actual_size = current_bytes / (1024 * 1024)
    num_rows = id_counter - 1
    print(f"✓ {filename} generado: {actual_size:.2f} MB ({num_rows:,} registros)")
    return current_bytes


def main():
    print("="*80)
    print("GENERADOR DE ARCHIVOS ALTAMENTE COMPRIMIBLES")
    print("="*80)
    print()
    
    # Generar archivos
    log_size = generate_system_logs("system_logs.txt", size_mb=2)
    print()
    csv_size = generate_csv_dataset("sales_dataset.csv", size_mb=2)
    
    print()
    print("="*80)
    print("✅ ARCHIVOS GENERADOS EXITOSAMENTE")
    print("="*80)
    print()
    print("Archivos creados:")
    print(f"  1. system_logs.txt - {log_size/(1024*1024):.2f} MB")
    print(f"  2. sales_dataset.csv - {csv_size/(1024*1024):.2f} MB")
    print()
    print("Estos archivos tienen alta redundancia y deberían comprimir bien con LZ78.")
    print("Usa test_large_compression.py para probar cada uno.")
    print()
    print("Para probar:")
    print("  1. Edita test_large_compression.py")
    print("  2. Cambia test_file = 'system_logs.txt' o 'sales_dataset.csv'")
    print("  3. Ejecuta: python test_large_compression.py")


if __name__ == "__main__":
    main()
