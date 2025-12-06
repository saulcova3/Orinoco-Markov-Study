import pandas as pd
import os
import glob
from datetime import datetime

# Configuración de paths
CARPETA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_RAW = os.path.join(CARPETA_BASE, 'data', 'raw_data')
CARPETA_METADATA = os.path.join(CARPETA_BASE, 'data', 'metadata')
CARPETA_MASTER = os.path.join(CARPETA_BASE, 'data', 'master')
ARCHIVO_MASTER = os.path.join(CARPETA_MASTER, 'master_database_orinoco.csv')
ARCHIVO_METADATA = os.path.join(CARPETA_METADATA, 'metadata_estaciones_orinoco.csv')

def crear_carpetas():
    """Crea automáticamente todas las carpetas necesarias"""
    os.makedirs(CARPETA_MASTER, exist_ok=True)
    print(f"📁 Carpeta master: {CARPETA_MASTER}")

def cargar_metadata():
    """Carga el archivo de metadata con información de las estaciones"""
    try:
        if not os.path.exists(ARCHIVO_METADATA):
            print("❌ No se encontró el archivo de metadata")
            return None
        
        df_meta = pd.read_csv(ARCHIVO_METADATA)
        print(f"✅ Metadata cargada: {len(df_meta)} estaciones")
        return df_meta
        
    except Exception as e:
        print(f"❌ Error cargando metadata: {e}")
        return None

def procesar_archivo_estacion(archivo, df_metadata):
    """Procesa un archivo individual y lo enriquece con metadata"""
    try:
        # Extraer ID del nombre del archivo
        estacion_id = os.path.basename(archivo).replace('.csv', '')
        
        # Cargar datos de la estación CON SEPARADOR CORRECTO
        df_estacion = pd.read_csv(archivo, sep=';')
        
        # DEBUG: Mostrar columnas para el primer archivo
        if estacion_id == '17241':  # Primer archivo
            print(f"   📋 Columnas encontradas: {list(df_estacion.columns)}")
            print(f"   📊 Primeras filas:")
            print(df_estacion.head())
        
        # Agregar ID de estación como columna
        df_estacion['estacion_id'] = estacion_id
        
        # Convertir estacion_id a int para comparar con metadata
        try:
            estacion_id_int = int(estacion_id)
            meta_estacion = df_metadata[df_metadata['dahiti_id'] == estacion_id_int]
        except ValueError:
            print(f"   ⚠️  ID no numérico: {estacion_id}")
            meta_estacion = pd.DataFrame()
        
        if not meta_estacion.empty:
            # Agregar todas las columnas de metadata
            for columna in ['target_name', 'continent', 'country', 
                          'type', 'longitude', 'latitude']:
                if columna in meta_estacion.columns:
                    df_estacion[columna] = meta_estacion[columna].iloc[0]
        
        print(f"✅ Procesada: {estacion_id} ({len(df_estacion)} registros)")
        return df_estacion
        
    except Exception as e:
        print(f"❌ Error procesando {archivo}: {e}")
        return None

def crear_master_database():
    """Crea la base de datos maestra uniendo todos los archivos"""
    # Crear carpetas necesarias
    crear_carpetas()
    
    # Cargar metadata
    df_metadata = cargar_metadata()
    if df_metadata is None:
        return
    
    # Encontrar todos los archivos CSV en raw_data
    archivos = glob.glob(os.path.join(CARPETA_RAW, '*.csv'))
    
    if not archivos:
        print("❌ No se encontraron archivos en raw_data/")
        return
    
    print(f"📊 Encontrados {len(archivos)} archivos para procesar")
    print("=" * 60)
    
    # Procesar cada archivo
    datos_combinados = []
    
    for i, archivo in enumerate(archivos, 1):
        print(f"[{i}/{len(archivos)}] Procesando: {os.path.basename(archivo)}")
        
        df_procesado = procesar_archivo_estacion(archivo, df_metadata)
        if df_procesado is not None:
            datos_combinados.append(df_procesado)
    
    if not datos_combinados:
        print("❌ No se pudieron procesar archivos")
        return
    
    # Combinar todos los datos
    print("🔄 Combinando todos los datos...")
    df_master = pd.concat(datos_combinados, ignore_index=True)
    
    # Guardar master database
    df_master.to_csv(ARCHIVO_MASTER, index=False, encoding='utf-8')
    
    # Mostrar resumen (VERIFICAR COLUMNAS EXISTENTES)
    print("=" * 60)
    print("🎉 MASTER DATABASE CREADA:")
    print(f"   📁 Ubicación: {ARCHIVO_MASTER}")
    print(f"   📊 Total registros: {len(df_master):,}")
    print(f"   🏭 Total estaciones: {df_master['estacion_id'].nunique()}")
    
    # Verificar qué columnas de fecha existen
    columnas_fecha = [col for col in df_master.columns if 'date' in col.lower() or 'datetime' in col.lower()]
    if columnas_fecha:
        col_fecha = columnas_fecha[0]
        print(f"   📅 Rango temporal: {df_master[col_fecha].min()} a {df_master[col_fecha].max()}")
    else:
        print("   ⚠️  No se encontraron columnas de fecha")
    
    print(f"   📋 Columnas disponibles: {list(df_master.columns)}")
    
    return df_master

def analizar_master_database():
    """Análisis rápido de la base de datos maestra"""
    if not os.path.exists(ARCHIVO_MASTER):
        print("❌ No existe la master database")
        return
    
    df_master = pd.read_csv(ARCHIVO_MASTER)
    
    print("\n📈 ANÁLISIS RÁPIDO MASTER DATABASE:")
    print("=" * 50)
    print(f"📊 Registros totales: {len(df_master):,}")
    print(f"🏭 Estaciones únicas: {df_master['estacion_id'].nunique()}")
    print(f"🇻🇪 Estaciones en Venezuela: {len(df_master[df_master['country'] == 'Venezuela']):,}")
    print(f"🇨🇴 Estaciones en Colombia: {len(df_master[df_master['country'] == 'Colombia']):,}")
    
    # CORRECCIÓN: Usar 'datetime' en lugar de 'date'
    print(f"📅 Rango fechas: {df_master['datetime'].min()} a {df_master['datetime'].max()}")
    
    # También verificar si existe la columna water_level
    if 'water_level' in df_master.columns:
        print(f"🌊 Rango niveles agua: {df_master['water_level'].min():.2f} a {df_master['water_level'].max():.2f} m")

if __name__ == "__main__":
    # Crear la master database
    df_master = crear_master_database()
    
    # Análisis rápido
    if df_master is not None:
        analizar_master_database()