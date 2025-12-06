# Caso de estudio: cadenas de Markov aplicadas al Río Orinoco

## 🌊 Contexto hidrológico

El río Orinoco se caracteriza por ser de gran extensión y por presentar patrones cíclicos de crecimiento y decrecimiento. Por experiencia, tanto las crecidas como las bajadas en el nivel del agua cumplen con una cualidad de sumo interés: **su nivel futuro no depende de toda su historia hidrológica, sino principalmente de su estado actual** (cuánta agua contiene ahora, la intensidad de las lluvias recientes, fenómenos meteorológicos como el niño y la niña y la evaporación presente).

Así como un periodo de lluvias intensas hoy determina una crecida inminente con mayor peso que lo ocurrido hace años, el río "recuerda" con especial énfasis su condición hidrológica más reciente para definir su siguiente fase, haciendo de su dinámica **un proceso con memoria a corto plazo**.

Partiendo de esa premisa, se plantea la idea de estudiar de forma descriptiva y modelar el comportamiento de las crecidas/bajadas **como un proceso estocástico markoviano**.

## 📡 Obtención de datos

Para este estudio implementamos data histórica recopilada entre los años **2002 y 2025** por la **Universidad Técnica de Munich**. Dicha data fue recopilada a través de consultas a la **DAHITI** (Database for Hydrological Time Series of Inland Waters) con ayuda de su API.

### 🔍 Detalles técnicos
- **Fechas de consulta**: 24/08/2025 y 25/08/2025
- **API**: DAHITI REST API v2
- **Seguridad**: Variables de entorno protegidas
- **Formato de salida**: CSV estandarizado

## 📍 Estaciones monitoreadas

Las consultas incluyeron **70 estaciones virtuales** a lo largo del Río Orinoco:

```
1120: Orinoco, River
1121: Orinoco, River
1122: Orinoco, River
1207: Orinoco, River
1208: Orinoco, River
1209: Orinoco, River
1255: Orinoco, River
1256: Orinoco, River
1257: Orinoco, River
1258: Orinoco, River
1259: Orinoco, River
1260: Orinoco, River
6739: Orinoco, River
7823: Orinoco, River
9222: Orinoco, River
9223: Orinoco, River
9365: Orinoco, River
9368: Orinoco, River
9395: Orinoco, River
9396: Orinoco, River
9398: Orinoco, River
9400: Orinoco, River
13271: Orinoco, River
13272: Orinoco, River
13273: Orinoco, River
13274: Orinoco, River
13275: Orinoco, River
13276: Orinoco, River
13277: Orinoco, River
13500: Orinoco, River
13504: Orinoco, River
13505: Orinoco, River
13506: Orinoco, River
13507: Orinoco, River
13509: Orinoco, River
13510: Orinoco, River
14284: Orinoco, River
14478: Orinoco, River
15030: Orinoco, River
15310: Orinoco, River
15436: Orinoco, River
15677: Orinoco, River
15811: Orinoco, River
16058: Orinoco, River
16344: Orinoco, River
16345: Orinoco, River
16705: Orinoco, River
16708: Orinoco, River
16864: Orinoco, River
17096: Orinoco, River
17241: Orinoco, River
17492: Orinoco, River
17627: Orinoco, River
17628: Orinoco, River
17630: Orinoco, River
19802: Orinoco, River
19803: Orinoco, River
19804: Orinoco, River
19805: Orinoco, River
19806: Orinoco, River
23575: Orinoco, River
23576: Orinoco, River
23577: Orinoco, River
23578: Orinoco, River
23579: Orinoco, River
23580: Orinoco, River
23581: Orinoco, River
23582: Orinoco, River
27203: Orinoco, River
18786: Orinooco, River
```

## 📊 Estructura de datos

Cada estación presentó:

- **🆔 Número de identificación** único
- **📍 Coordenadas** de latitud y longitud
- **🇺🇳 País y continente** de origen
- **📅 Archivo CSV** con:
  - Registro de mediciones del nivel del río
  - Cálculo del margen de error por medición
  - Fechas correspondientes del registro

## 🔄 Pipeline técnico

### 1. **Extracción (`consultas_API.py`)**
- Conexión segura a API DAHITI
- Filtrado de estaciones del Orinoco principal
- Generación de metadatos (`metadata_estaciones_orinoco.csv`)

### 2. **Descarga (`descargar_data.py`)**
- Descarga masiva de 70 archivos CSV
- Manejo de errores y reintentos automáticos
- Reporte de descarga con validación

### 3. **Transformación (`crear_master_database.py`)**
- Consolidación de 70 archivos en base de datos única
- Enriquecimiento con metadatos geográficos
- Creación de `master_database_orinoco.csv` (9,455 registros)

## 📈 Resultados del pipeline

- **📁 Total archivos procesados**: 70
- **📊 Registros consolidados**: 9,455
- **📅 Rango temporal**: 2002-2025 (23 años)
- **🌍 Cobertura**: Venezuela y Colombia
- **⚡ Tasa de éxito**: 100% en descarga

## 📓 Análisis en Jupyter Notebooks

### **📊 `explore_1_AJuste_data.ipynb` - Calibración por punto de anclaje**

#### **📍 Objetivo**
Encontrar la estación más cercana a Ciudad Bolívar y ajustar sus datos mediante el **método del punto de anclaje** para obtener una serie temporal representativa.

#### **🔍 Metodología**
1. **Geolocalización**: Uso de `geopy` para calcular distancias desde Ciudad Bolívar (8.1333, -63.5333)
2. **Selección**: Estación 15436 identificada como la más cercana
3. **Calibración**: Ajuste basado en nivel promedio reportado por HIDROMET-UCV (14.03 msnm, septiembre 2024)
4. **Validación**: Comparación visual serie cruda vs calibrada

#### **📈 Resultados clave**
- **Estación seleccionada**: 15436 (más cercana a Ciudad Bolívar)
- **Método**: Punto de anclaje con referencia hidrométrica oficial
- **Output**: Serie temporal calibrada lista para análisis

#### **⚠️ Limitaciones reconocidas**
1. No considera factores locales geográficos/estacionales
2. Reajuste depende únicamente del desfase existente
3. Recomendado solo para distancias cortas

---

### **🔮 `explore_2_Modelado_matemático.ipynb` - Análisis Markoviano**

#### **🎯 Objetivo**
Modelar el comportamiento del Orinoco como **proceso estocástico markoviano**, identificando patrones de persistencia en subidas/bajadas del nivel del agua.

#### **🔄 Pipeline de análisis**
1. **Preprocesamiento**:
   - Consolidación: `estacion_id + (lat, lon) + sufijo regional`
   - Clasificación regional: HO (Alto), MO (Medio), LO (Bajo), Delta
   - Segmentación temporal: Épocas de lluvia/sequía por región

2. **Segmentación**:
   - **Espacial**: 4 regiones hidrológicas
   - **Temporal**: 8 segmentos hidro-temporales (región × época)

3. **Modelado Markoviano**:
   - Discretización: Estados binarios (1=sube, 0=baja)
   - Cálculo: Matrices de transición 2×2 por región
   - Métrica clave: **Persistencia** = (P(0→0) + P(1→1)) / 2

#### **📊 Hallazgos principales**

##### **Persistencia por región (orden descendente)**
```
1. HO (Alto Orinoco):    0.698  ← Mayor predictibilidad
2. LO (Bajo Orinoco):    0.696
3. MO (Orinoco Medio):   0.638
4. Delta:                0.625  ← Mayor variabilidad
```

##### **Estadísticas globales**
- **Transiciones analizadas**: 9,241 (muestra estadísticamente robusta)
- **Estaciones**: 70/70 aportaron datos (cobertura completa)
- **Tendencia global**: 54.5% probabilidad de bajada
- **Persistencias**: >0.62 en todas las regiones (señal clara detectable)

#### **💡 Interpretación hidrológica**

##### **🏔️ Alto Orinoco (HO)**
- Comportamiento más "conservador"
- Responde lentamente a cambios
- **73.7%** probabilidad de continuar bajando si ya está bajando
- Ideal para predicciones a corto plazo

##### **🌊 Delta**
- Influencia de mareas evidente
- Comportamiento más errático
- Mayor probabilidad de cambio de tendencia
- Requiere monitoreo más frecuente

#### **🚀 Recomendaciones operativas**

##### **Para sistema de alertas**
```python
# Lógica recomendada:
if region in ['HO', 'LO'] and estado_actual == 'bajando':
    alerta = "Alta probabilidad de continuar bajando (>70%)"
elif region == 'Delta':
    alerta = "Monitoreo intensivo - alta variabilidad"
```

##### **Para gestión del río**
1. **HO/LO**: Enfocar recursos en tendencias establecidas
2. **Delta**: Monitoreo más frecuente (mayor incertidumbre)
3. **Umbral acción**: >70% persistencia en bajadas

##### **Para predicción**
- Modelo más confiable: "Si está bajando, probablemente siga bajando"
- Menor confianza en cambios bruscos de subida a bajada
- Patrones consistentes entre regiones → resultados confiables

#### **✅ Validación del modelo**
- **Cobertura**: 100% de estaciones analizadas
- **Muestra**: 9,241 transiciones (robustez estadística)
- **Consistencia**: Patrones coherentes entre regiones
- **Aplicabilidad**: Resultados útiles para gestión hidrológica

---

## 🔬 **Síntesis metodológica**

### **Del dato crudo al insight operativo**
```
Datos satelitales → Pipeline ETL → Segmentación → Matrices Markov → Recomendaciones
      (API DAHITI)    (scripts/)   (notebooks/)    (análisis)      (gestión)
```

### **Valor agregado del análisis**
1. **Científico**: Validación empírica de propiedad markoviana en sistema fluvial
2. **Práctico**: Herramientas concretas para gestión hidrológica
3. **Metodológico**: Framework reproducible para otros ríos
4. **Operativo**: Sistema de alertas basado en probabilidades calculadas

---

**📅 Análisis completado en Diciembre 2024**  
**🔬 Metodología: Procesos estocásticos + Hidrología aplicada**  
**🎯 Objetivo logrado: Modelado predictivo para gestión del Río Orinoco**

## 📚 Fuentes académicas

**Schwatke, C., Dettmering, D., Bosch, W., and Seitz, F.:**  
*DAHITI - an innovative approach for estimating water level time series over inland waters using multi-mission satellite altimetry*,  
Hydrol. Earth Syst. Sci., 19, 4345-4364, doi:10.5194/hess-19-4345-2015, 2015

**Arévalo, J., Gil, A., & Mundaray, R.** (2024, septiembre).  
*Comportamiento de los niveles del río Orinoco: Septiembre 2024*.  
Hidromet UCV.  
https://hidromet-ucv.org.ve/comportamiento-de-los-niveles-del-rio-orinoco-septiembre-2024/

## 🏗️ Estructura del proyecto

```
orinorkov/
├── scripts/                    # Pipeline automatizado
│   ├── consultas_API.py       # Integración API DAHITI
│   ├── descargar_data.py      # Descarga masiva (70 CSV)
│   └── crear_master_database.py  # Consolidación ETL
├── notebooks/                  # Análisis exploratorio
│   ├── explore_1_AJuste_data.ipynb
│   └── explore_2_Modelado_matemático.ipynb
├── data/                       # Datasets procesados
│   ├── raw_data/              # 70 archivos CSV originales
│   ├── metadata/              # Metadatos de estaciones
│   ├── master/                # Dataset consolidado
│   └── clean_data/            # Datos listos para modelado
├── .env.example                # Template para API keys
├── .gitignore                  # Configuración de seguridad
├── requirements.txt            # Dependencias Python
└── README.md                   # Esta documentación
```

## 🚀 Instalación y uso

```bash
# 1. Clonar repositorio
git clone https://github.com/saulcova3/Orinoco-Markov-Study.git

# 2. Configurar entorno
python -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API key
cp .env.example .env
# Editar .env con tu API key de DAHITI

# 5. Ejecutar pipeline
python scripts/consultas_API.py
python scripts/descargar_data.py
python scripts/crear_master_database.py
```

## 🔐 Seguridad

- **🔑 API Keys**: Almacenadas en `.env` (excluido de Git)
- **📄 Template**: `.env.example` para configuración colaborativa
- **🚫 Ignorados**: `.env`, `.venv/`, `__pycache__/`, datos sensibles

---

**📅 Proyecto realizado en Diciembre 2024**  
**👨‍💻 Desarrollado por Saul Cova**  
**🌐 Repositorio: [github.com/saulcova3/Orinoco-Markov-Study](https://github.com/saulcova3/Orinoco-Markov-Study)**
