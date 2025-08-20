
from math import pi, log, tan
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, WMTSTileSource

output_notebook()

# --- Conversión lat/lon a WebMercator
R = 6378137
def lonlat_to_mercator(lon, lat):
    x = lon * (pi/180) * R
    y = R * log(tan((pi/4) + (lat*pi/360)))
    return x, y

# --- Estaciones mareográficas (aproximadas)
estaciones = [
    # Pacífico
    {"nombre": "La Paz", "lat": 24.142, "lon": -110.310},
    {"nombre": "Mazatlán", "lat": 23.216, "lon": -106.420},
    {"nombre": "Puerto Vallarta", "lat": 20.653, "lon": -105.225},
    {"nombre": "Manzanillo", "lat": 19.053, "lon": -104.316},
    {"nombre": "Lázaro Cárdenas", "lat": 17.958, "lon": -102.198},
    {"nombre": "Zihuatanejo", "lat": 17.635, "lon": -101.550},
    {"nombre": "Acapulco", "lat": 16.863, "lon": -99.882},
    {"nombre": "Puerto Ángel", "lat": 15.670, "lon": -96.495},
    {"nombre": "Huatulco", "lat": 15.768, "lon": -96.122},
    {"nombre": "Salina Cruz", "lat": 16.176, "lon": -95.198},
    {"nombre": "Puerto Chiapas", "lat": 14.708, "lon": -92.403},

    # Golfo / Caribe
    {"nombre": "Tuxpan", "lat": 20.950, "lon": -97.400},
    {"nombre": "Veracruz", "lat": 19.200, "lon": -96.133},
    {"nombre": "Alvarado", "lat": 18.780, "lon": -95.766},
    {"nombre": "Sánchez Magallanes", "lat": 18.000, "lon": -93.850},
    {"nombre": "Río Grijalva", "lat": 18.400, "lon": -93.183},
    {"nombre": "Frontera", "lat": 18.533, "lon": -92.650},
    {"nombre": "Ciudad del Carmen", "lat": 18.633, "lon": -91.833},
    {"nombre": "Lerma", "lat": 19.850, "lon": -90.533},
    {"nombre": "Celestún", "lat": 20.867, "lon": -90.400},
    {"nombre": "Sisal", "lat": 21.166, "lon": -90.033},
    {"nombre": "Progreso", "lat": 21.283, "lon": -89.667},
    {"nombre": "Telchac", "lat": 21.350, "lon": -89.283},
    {"nombre": "Isla Mujeres", "lat": 21.233, "lon": -86.733},
    {"nombre": "Puerto Morelos", "lat": 20.850, "lon": -86.883},
    {"nombre": "Sian Ka’an", "lat": 19.333, "lon": -87.433},
]

# --- Convertir todas a Mercator
xs, ys, nombres = [], [], []
for est in estaciones:
    x, y = lonlat_to_mercator(est["lon"], est["lat"])
    xs.append(x); ys.append(y); nombres.append(est["nombre"])

source = ColumnDataSource(dict(x=xs, y=ys, nombre=nombres))

# --- Crear figura
tile_provider = WMTSTileSource(
    url="http://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
)

p = figure(
    x_axis_type="mercator", y_axis_type="mercator",
    width=900, height=600,
    title="Estaciones Mareográficas UNAM (aprox.)"
)
p.add_tile(tile_provider)

# --- Marcadores
r = p.scatter(x="x", y="y", size=10, source=source, color="blue", alpha=0.8)

# --- Hover para mostrar nombre
hover = HoverTool(tooltips=[("Estación", "@nombre")], renderers=[r])
p.add_tools(hover)

# Mostrar mapa
show(p)

