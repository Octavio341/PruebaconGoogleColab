# --- mapa.py ---
from math import pi, log, tan
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, WMTSTileSource

R = 6378137
def lonlat_to_mercator(lon, lat):
    x = lon * (pi/180) * R
    y = R * log(tan((pi/4) + (lat*pi/360)))
    return x, y

def graficar_estaciones():
    estaciones = [
        {"nombre": "La Paz", "lat": 24.142, "lon": -110.310},
        {"nombre": "Veracruz", "lat": 19.200, "lon": -96.133},
        {"nombre": "Progreso", "lat": 21.283, "lon": -89.667},
    ]

    xs, ys, nombres = [], [], []
    for est in estaciones:
        x, y = lonlat_to_mercator(est["lon"], est["lat"])
        xs.append(x); ys.append(y); nombres.append(est["nombre"])

    source = ColumnDataSource(dict(x=xs, y=ys, nombre=nombres))

    tile_provider = WMTSTileSource(
        url="https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
    )

    p = figure(x_axis_type="mercator", y_axis_type="mercator",
               width=900, height=600,
               title="Estaciones Mareográficas UNAM (aprox.)")
    p.add_tile(tile_provider)

    r = p.scatter(x="x", y="y", size=10, source=source, color="blue", alpha=0.8)

    hover = HoverTool(tooltips=[("Estación", "@nombre")], renderers=[r])
    p.add_tools(hover)

    return p
