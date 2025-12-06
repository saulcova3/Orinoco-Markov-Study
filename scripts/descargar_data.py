import requests
import time
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Obtener API key de forma segura
API_KEY = os.getenv("DAHITI_API_KEY")

# Validar que la key existe
if not API_KEY or API_KEY == "your_actual_api_key_here":
    raise ValueError(
        "❌ ERROR: DAHITI_API_KEY no configurada.\n"
        "Por favor:\n"
        "1. Copia '.env.example' a '.env'\n"
        "2. Agrega tu API key real en '.env'\n"
        "3. Asegúrate de que '.env' esté en '.gitignore'"
    )

# Configuración
CARPETA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
CARPETA_DATOS = os.path.join(CARPETA_BASE, 'data', 'raw_data')              # data/raw_data/
CARPETA_SCRIPTS = os.path.dirname(os.path.abspath(__file__))                # scripts/
ARCHIVO_IDS = os.path.join(CARPETA_SCRIPTS, 'resultados_consulta_orinoco.txt')  # scripts/resultados_consulta_orinoco

DELAY_ENTRE_DESCARGAS = 2
OUTPUT_FORMAT = 'csv'

def crear_carpetas():
    """Crea automáticamente todas las carpetas necesarias"""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    print(f"📁 Carpeta de datos: {CARPETA_DATOS}")

def descargar_estacion(dahiti_id, carpeta_destino):
    """
    Descarga los datos de una estación individual
    Retorna: (éxito, mensaje)
    """
    try:
        parametros = {
            'api_key': API_KEY,
            'dahiti_id': dahiti_id,
            'format': OUTPUT_FORMAT
        }
        
        print(f"   📥 Descargando estación {dahiti_id}...")
        response = requests.post(
            'https://dahiti.dgfi.tum.de/api/v2/download-water-level/',
            json=parametros,
            timeout=30
        )
        
        if response.status_code == 200:
            # Guardar archivo
            nombre_archivo = f"{dahiti_id}.csv"
            ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
            
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                archivo.write(response.text)
            
            return True, f"✅ {dahiti_id}.csv"
            
        else:
            return False, f"❌ Error HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def descargar_lotes(lista_ids, carpeta_destino):
    """
    Descarga múltiples estaciones con manejo de errores
    """
    print(f"🚀 Iniciando descarga de {len(lista_ids)} estaciones...")
    print("=" * 60)
    
    resultados = {
        'exitosas': [],
        'fallidas': [],
        'errores': {}
    }
    
    for i, estacion_id in enumerate(lista_ids, 1):
        # Descargar estación
        exito, mensaje = descargar_estacion(estacion_id, carpeta_destino)
        
        if exito:
            resultados['exitosas'].append(estacion_id)
            print(f"[{i}/{len(lista_ids)}] {mensaje}")
        else:
            resultados['fallidas'].append(estacion_id)
            resultados['errores'][estacion_id] = mensaje
            print(f"[{i}/{len(lista_ids)}] {mensaje}")
        
        # Pausa entre descargas
        if i < len(lista_ids):
            time.sleep(DELAY_ENTRE_DESCARGAS)
    
    return resultados

def generar_reporte(resultados, carpeta_destino):
    """
    Genera reporte de la descarga
    """
    ruta_reporte = os.path.join(carpeta_destino, 'reporte_descarga.txt')
    
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE DESCARGA - RÍO ORINOCO\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Estaciones exitosas: {len(resultados['exitosas'])}\n")
        f.write(f"Estaciones fallidas: {len(resultados['fallidas'])}\n\n")
        
        f.write("ESTACIONES EXITOSAS:\n")
        f.write("-" * 30 + "\n")
        for id in resultados['exitosas']:
            f.write(f"{id}\n")
        
        f.write("\nESTACIONES FALLIDAS:\n")
        f.write("-" * 30 + "\n")
        for id in resultados['fallidas']:
            f.write(f"{id}: {resultados['errores'].get(id, 'Error desconocido')}\n")
    
    print(f"💾 Reporte guardado en: {ruta_reporte}")

def cargar_ids_desde_archivo(ruta_archivo):
    """
    Carga lista de IDs desde archivo de texto
    Formato esperado: 'ID: Nombre, River'
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            ids = []
            for linea in f:
                linea_limpia = linea.strip()
                
                # Saltar líneas vacías, encabezados y separadores
                if (not linea_limpia or 
                    linea_limpia.startswith('ESTACIONES') or 
                    linea_limpia.startswith('=')):
                    continue
                
                # Extraer el ID (primera parte antes de ':')
                if ':' in linea_limpia:
                    id_part = linea_limpia.split(':')[0].strip()
                    if id_part.isdigit():
                        ids.append(id_part)
            
            return ids
            
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        return []
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return []

# Ejecución principal
if __name__ == "__main__":
    # Crear automáticamente todas las carpetas necesarias
    crear_carpetas()
    
    # Cargar desde archivo (ruta relativa)
    ids_a_descargar = cargar_ids_desde_archivo(ARCHIVO_IDS)
    
    if not ids_a_descargar:
        print("❌ No hay IDs para descargar")
        print("💡 Ejecuta primero consultas_API.py para generar la lista")
    else:
        print(f"📋 IDs cargados: {len(ids_a_descargar)}")
        print(f"   Primeros 5: {ids_a_descargar[:5]}")
        print(f"   Últimos 5: {ids_a_descargar[-5:]}")
        
        confirmacion = input("\n¿Continuar con la descarga? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Descargar
            resultados = descargar_lotes(ids_a_descargar, CARPETA_DATOS)
            
            # Generar reporte
            generar_reporte(resultados, CARPETA_DATOS)
            
            # Resumen final
            print(f"\n🎉 DESCARGA COMPLETADA:")
            print(f"   ✅ Exitosas: {len(resultados['exitosas'])}")
            print(f"   ❌ Fallidas: {len(resultados['fallidas'])}")
        else:
            print("⏹️ Descarga cancelada")