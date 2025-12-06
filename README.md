Caso de estudio: cadenas de Markov aplicadas al Río Orinoco.

El río Orinoco se caracteriza por ser de gran extensión y por presentar patrones cíclicos de crecimiento y decrecimiento. Por experiencia, tanto las crecidas como las bajadas en el nivel del agua cumplen con una cualidad de sumo interés; su nivel futuro no depende de toda su historia hidrológica, sino principalmente de su estado actual (cuánta agua contiene ahora, la intensidad de las lluvias recientes, fenómenos meteorológicos como el niño y la niña y la evaporación presente).

Así como un periodo de lluvias intensas hoy determina una crecida inminente con mayor peso que lo ocurrido hace años, el río "recuerda" con especial énfasis su condición hidrológica más reciente para definir su siguiente fase, haciendo de su dinámica un proceso con memoria a corto plazo.

Partiendo de esa premisa, se plantea la idea de estudiar de forma descriptiva y modelar el comportamiento de las crecidas/bajadas como un proceso estocástico markoviano. Para ello implementaremos data histórica recopilada entre los años 2002 y 2025 por la Universidad Técnica de Munich. Dicha data fue recopilada a través de consultas a la DAHITI (Database for Hydrological Time Series of Inland Waters) con ayuda de su API. 

Las consultas se hicieron los días 24/08/2025 y 25/20/2025, e incluyeron las siguientes estaciones virtuales:

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

Cada estación presentó un número de identificación, sus coordenadas de latitud y longitud, su país y continente de orígen. Además, para cada estación se descargó un archivo .csv con un registro de distintas mediciones del nivel del río (junto a un cálculo del márgen de error cada medición) y las fechas correspondientes del registro.

Fuentes:

Schwatke, C., Dettmering, D., Bosch, W., and Seitz, F.: DAHITI - an innovative approach for estimating water level time series over inland waters using multi-mission satellite altimetry: , Hydrol. Earth Syst. Sci., 19, 4345-4364, doi:10.5194/hess-19-4345-2015, 2015 

Arévalo, J., Gil, A., & Mundaray, R. (2024, septiembre). Comportamiento de los niveles del río Orinoco: Septiembre 2024. Hidromet UCV. https://hidromet-ucv.org.ve/comportamiento-de-los-niveles-del-rio-orinoco-septiembre-2024/