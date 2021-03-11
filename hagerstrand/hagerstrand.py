"""Main module."""
import os
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, TileLayer, basemaps, basemap_to_tiles

# Credit: Dr. Qiusheng Wu
class Map(ipyleaflet.Map):

    def __init__(self, **kwargs):

        if "center" not in kwargs:
            kwargs["center"] = [40, -100]

        if "zoom" not in kwargs:
            kwargs["zoom"] = 4

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(**kwargs)

        if "height" not in kwargs:
            self.layout.height = "600px"
        else:
            self.layout.height = kwargs["height"]

        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))


        if "google_map" not in kwargs:
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Maps",
            )
            self.add_layer(layer)
        else:
            if kwargs["google_map"] == "ROADMAP":
                layer = TileLayer(
                    url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                    attribution="Google",
                    name="Google Maps",
                )
                self.add_layer(layer)
            elif kwargs["google_map"] == "HYBRID":
                layer = TileLayer(
                    url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                    attribution="Google",
                    name="Google Satellite"
                )
                self.add_layer(layer)

        if "basemap" not in kwargs:
            layer = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)
            self.add_layer(layer)
        else:
            layer = basemap_to_tiles(kwargs["basemap"])
            self.add_layer(layer)


    def add_geojson(self, in_geojson, style=None, layer_name="Untitled"):

        import json

        if isinstance(in_geojson, str):

            if not os.path.exists(in_geojson):
                raise FileNotFoundError("The provided GeoJSON file could not be found.")

            with open(in_geojson) as f:
                data = json.load(f)
        
        elif isinstance(in_geojson, dict):
            data = in_geojson
        
        else:
            raise TypeError("The input geojson must be a type of str or dict.")

        if style is None:
            style = {
                "stroke": True,
                "color": "#000000",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "#0000ff",
                "fillOpacity": 0.4,
            }

        geo_json = ipyleaflet.GeoJSON(data=data, style=style, name=layer_name)
        self.add_layer(geo_json) 

# Credit: Dr. Qiusheng Wu
    def add_shapefile(self, in_shp, style=None, layer_name="Untitled"):

        geojson = shp_to_geojson(in_shp)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

    def add_gmapjson(self, in_json, style=None, layer_name="Untitled"):

        geojson = gmapjson_to_geojson(in_json)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

# Credit: Dr. Qiusheng Wu
def shp_to_geojson(in_shp, out_geojson=None):

    import json
    import shapefile

    in_shp = os.path.abspath(in_shp)

    if not os.path.exists(in_shp):
        raise FileNotFoundError("The provided shapefile could not be found.")

    sf = shapefile.Reader(in_shp)
    geojson = sf.__geo_interface__

    if out_geojson is None:
        return geojson
    else:
        out_geojson = os.path.abspath(out_geojson)
        out_dir = os.path.dirname(out_geojson)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(out_geojson, "w") as f:
            f.write(json.dumps(geojson))    

def gmapjson_to_geojson(in_gmapjson, out_gmapgeojson=None):

    import json
    import datetime
    
    in_gmapjson = os.path.abspath(in_gmapjson)

    if not os.path.exists(in_gmapjson):
       raise FileNotFoundError("The provided json could not be found.")

    with open(in_gmapjson) as f:
        data = json.load(f)
    
    for item in data["locations"]:
        item["latitudeE7"] = item["latitudeE7"] * 0.0000001
        item["longitudeE7"] = item["longitudeE7"] * 0.0000001
        item["timestampMs"] = datetime.datetime.fromtimestamp(int(item["timestampMs"])/1000.0)
        item["timestampMs"] = item["timestampMs"].strftime('%Y-%m-%d %H:%M:%S') 
    
    data_intermediate = data["locations"]

    geojson = {
        "type": "FeatureCollection",
        "features": [
        {
            "type": "Feature",
            "geometry" : {
                "type": "Point",
                "coordinates": [d["longitudeE7"], d["latitudeE7"]],
                },
            "properties" : d,
        } for d in data_intermediate]
    }

    if out_gmapgeojson is None:
        return geojson
    else:
        out_gmapgeojson = os.path.abspath(out_gmapgeojson)
        out_dir = os.path.dirname(out_gmapgeojson)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(out_gmapgeojson, "w") as f:
            f.write(json.dumps(geojson)) 

