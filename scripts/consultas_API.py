import requests
import time
import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv 

# Cargar variables desde .env
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
CARPETA_SCRIPTS = os.path.dirname(os.path.abspath(__file__))                # scripts/
CARPETA_METADATA = os.path.join(CARPETA_BASE, 'data', 'metadata')           # data/metadata/


def crear_carpetas():
    """Crea automáticamente todas las carpetas necesarias"""
    os.makedirs(CARPETA_METADATA, exist_ok=True)
    print(f"📁 Carpeta de metadata: {CARPETA_METADATA}")

def buscar_estaciones_orinoco():
    """Esta función hace la consulta a la API"""
    url = 'https://dahiti.dgfi.tum.de/api/v2/list-targets/'
    parametros = {
        'api_key': API_KEY,
        'basin': 'Orinoco'
    }

    try:
        print("🔍 Buscando estaciones del Orinoco...")
        response = requests.post(url, data=parametros, timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la búsqueda: {e}")
        return None

def filtrar_orinoco_principal(datos):
    """Filtra solo las estaciones del Orinoco principal"""
    if not datos or 'data' not in datos:
        return []

    todas_estaciones = datos['data']
    patrones_incluir = ['Orinoco, River', 'Orinoco River', 'Río Orinoco', 'Rio Orinoco', 'Orinooco']
    patrones_excluir = ['Apure', 'Arauca', 'Meta', 'Guaviare', 'Caura', 'Casanare', 'Ventuari', 'Capanaparo', 'Inírida', 'Atabapo', 'Guaviare', 'Vichada', 'Tomo']
    
    orinoco_principal = []
    
    for estacion in todas_estaciones:
        nombre = estacion['target_name']
        es_principal = any(p.lower() in nombre.lower() for p in patrones_incluir)
        no_es_afluente = not any(p.lower() in nombre.lower() for p in patrones_excluir)
        
        if es_principal and no_es_afluente:
            orinoco_principal.append(estacion)
    
    return orinoco_principal

def crear_csv_maestro(estaciones, nombre_archivo='metadata_estaciones_orinoco.csv'):
    """Crea un CSV con todos los metadatos de las estaciones"""
    if not estaciones:
        print("❌ No hay estaciones para crear el CSV maestro")
        return
    
    ruta_csv = os.path.join(CARPETA_METADATA, nombre_archivo)
    
    campos = [
        'dahiti_id', 'target_name', 'continent', 
        'country', 'type', 'longitude', 'latitude'
    ]
    
    try:
        with open(ruta_csv, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            
            for estacion in estaciones:
                # Convertir None a string vacío para CSV
                fila = {}
                for campo in campos:
                    valor = estacion.get(campo)
                    fila[campo] = valor if valor is not None else ''
                writer.writerow(fila)
        
        print(f"💾 CSV maestro guardado en: {ruta_csv}")
        print(f"   📊 Total registros: {len(estaciones)}")
        
    except Exception as e:
        print(f"❌ Error creando CSV maestro: {e}")

def mostrar_resultados_detallados(datos_completos, datos_filtrados):
    """Muestra resultados con todos los metadatos"""
    total_estaciones = len(datos_completos['data']) if datos_completos else 0
    
    print(f"\n📊 RESULTADOS:")
    print(f"   • Estaciones totales de la cuenca: {total_estaciones}")
    print(f"   • Estaciones Orinoco principal: {len(datos_filtrados)}")
    
    print(f"\n🎯 DETALLE ESTACIONES ORINOCO PRINCIPAL:")
    print("=" * 100)
    print(f"{'ID':<8} {'Nombre':<25} {'País':<15} {'Tipo':<10} {'Latitud':<10} {'Longitud':<10}")
    print("=" * 100)
    
    for estacion in datos_filtrados:
        # Convertir None a 'N/A' para evitar errores de formato
        pais = estacion.get('country', 'N/A') or 'N/A'
        tipo = estacion.get('type', 'N/A') or 'N/A'
        latitud = estacion.get('latitude', 'N/A') or 'N/A'
        longitud = estacion.get('longitude', 'N/A') or 'N/A'
        
        print(f"{estacion['dahiti_id']:<8} "
              f"{estacion['target_name']:<25} "
              f"{pais:<15} "
              f"{tipo:<10} "
              f"{latitud:<10} "
              f"{longitud:<10}")

if __name__ == "__main__":
    # Crear automáticamente todas las carpetas necesarias
    crear_carpetas()
    
    # 1. Buscar todas las estaciones de la cuenca
    datos_completos = buscar_estaciones_orinoco()
    
    if datos_completos:
        # 2. Filtrar solo el Orinoco principal
        orinoco_principal = filtrar_orinoco_principal(datos_completos)
        
        # 3. Mostrar resultados detallados
        mostrar_resultados_detallados(datos_completos, orinoco_principal)
        
        # 4. Crear CSV maestro con metadatos completos
        crear_csv_maestro(orinoco_principal)
        
        # 5. Guardar también el archivo de texto simple (en scripts/)
        if orinoco_principal:
            ruta_txt = os.path.join(CARPETA_SCRIPTS, 'resultados_consulta_orinoco.txt')
            with open(ruta_txt, 'w', encoding='utf-8') as f:
                f.write("ESTACIONES - RÍO ORINOCO PRINCIPAL\n")
                f.write("=" * 50 + "\n")
                for estacion in orinoco_principal:
                    f.write(f"{estacion['dahiti_id']}: {estacion['target_name']}\n")
            
            print(f"\n💾 Lista simple guardada en: {ruta_txt}")