"""Main module for the hagerstrand package."""
import os
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, TileLayer, basemaps, basemap_to_tiles
from sklearn.neighbors import BallTree
import numpy as np


# Credit: Dr. Qiusheng Wu
class Map(ipyleaflet.Map):
    """This Map class inherits the ipyleaflet Map class.

    Args:
        ipyleaflet (ipyleaflet.Map()): An ipyleaflet map.
    """    
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
        """Adds a GeoJSON file to the map.

        Args:
            in_geojson (str): The file path to the input GeoJSON.
            style (dict, optional): The style for the GeoJSON layer. Defaults to None.
            layer_name (str, optional): The layer name for the GeoJSON layer. Defaults to "Untitled".

        Raises:
            FileNotFoundError: If the provided file path does not exist.
            TypeError: If the input GeoJSON is not a str.
        """        
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
        """Adds a shapefile to the map

        Args:
            in_shp (str): The file path to the input shapefile.
            style (dict, optional): The style for the shapefile. Defaults to None.
            layer_name (str, optional): The layer name for the shapefile layer. Defaults to "Untitled".
        """
        geojson = shp_to_geojson(in_shp)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

    def add_gmapjson(self, in_json, style=None, layer_name="Untitled"):
        """Adds a Google Map Location History JSON file to the map

        Args:
            in_json (str): The file path to the input JSON.
            style (dict, optional): The style for the JSON. Defaults to None.
            layer_name (str, optional): The layer name for the JSON layer. Defaults to "Untitled".
        """
        geojson = gmapjson_to_geojson(in_json)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

# Credit: Dr. Qiusheng Wu
def shp_to_geojson(in_shp, out_geojson=None):
    """Converts a shapefile to GeoJSON.

    Args:
        in_shp (str): The file path to the input shapefile.
        out_geojson (str, optional): The file path for the output GeoJSON. Defaults to None.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
    """
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
    """Converts a Google Map Location History JSON to GeoJSON.

    Args:
        in_gmapjson (str): The file path to the input JSON.
        out_gmapgeojson (str, optional): The file path for the output GeoJSON. Defaults to None.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
    """

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

def poly_centroid(in_poly_shp, orig_epsg=6576, change_crs=False, epsg=6576, out_shp=None):
    """Calculates the centroid of all polygons in a file or DataFrame or GeoDataFrame.
    
    Args:
        in_poly_shp (str|pd.DataFrame|gpd.GeoDataFrame): The file path or pd.DataFrame or gpd.GeoDataFrame to the input polygon layer.
        orig_epsg (int, optional): The epsg code for the coordinate system of your input polygon layer. Defaults to 6576 (NAD83(2011) Tennessee State Plane).)
        change_crs (bool, optional): A flag indicating whether the coordinate system should be changed. Defaults to False.
        epsg (int, optional): The epsg code for the coordinate system to be changed. Defaults to 6576 (NAD83(2011) Tennessee State Plane).
        out_shp (str, optional): The filepath for the output shapefile. Defaults to None; doesn't save.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
        TypeError: If the input geojson is not a str or dict.
    """           
    import geopandas as gpd  
    
    if isinstance(in_poly_shp, str):
        
        if not os.path.exists(in_poly_shp):
            raise FileNotFoundError("The provided shapefile could not be found.")        
        
        orig_crs = "epsg:" + str(orig_epsg)
        poly = gpd.read_file(in_poly_shp, crs=orig_crs)
        points = poly.copy()
        
    elif isinstance(in_poly_shp, gpd.GeoDataFrame):
        points = in_poly_shp.copy()
    
    elif isinstance(in_poly_shp, pd.DataFrame):
        points = in_poly_shp.copy()
    
    else:
        raise TypeError("The input polygon layer must be a type of str, pandas.DataFrame, or geopandas.GeoDataFrame.")
    
    if change_crs:
        epsg_str = "epsg:" + str(epsg)
        poly = poly.to_crs(epsg_str)
    
    points.crs = poly.crs
    print("The coordinate system for the centroids is: " + str(points.crs))
    print("The coordinate system for the polygons is: " + str(poly.crs))
    points.geometry = points['geometry'].centroid
    
    if out_shp is not None:
        points.to_file(out_shp)

    return points

def csv_to_gdf(in_csv, index_col=None, latloncols=["latitude","longitude"], in_epsg=4326, out_epsg=6576, out_shp=None):
    """Converts a spreadsheet with latitude and longitude values to a geopandas.GeoDataFrame

    Args:
        in_csv (str): The file path to the input csv.
        index_col (int, optional): The index column. Defaults to None.
        latloncols (list, optional): The columns of y and x (e.g. lat, lon) as a list. Defaults to ["latitude","longitude"].
        in_epsg (int, optional): The EPSG code of the csv. Defaults to 4326 (WGS84).
        out_epsg (int, optional): The EPSG code of the output, if desired. Defaults to 6576 (NAD83(2011) State Plane Tennessee).
        out_shp (str, optional): The filepath for the output shapefile. Defaults to None; doesn't save.

    Returns:
        poi (gpd.GeoDataFrame): The output geopandas.GeoDataFrame.
    """
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    
    if index_col is not None:
        poi = pd.read_csv(in_csv, index_col=index_col)
    else:
        poi = pd.read_csv(in_csv)

    poi["ycoord"] = poi[latloncols[0]].astype(float)
    poi["xcoord"] = poi[latloncols[1]].astype(float)
    epsg_i = "epsg:" + str(in_epsg)
    poi = gpd.GeoDataFrame(
        poi, geometry = [Point(x,y) for x, y in zip(poi.xcoord, poi.ycoord)], crs = epsg_i)
    
    epsg_o = "epsg:" + str(out_epsg)
    poi = poi.to_crs({"init":epsg_o})
    
    if out_shp is not None:
        poi.to_file(out_shp)  

    return poi

def get_nearest(src_points, candidates, metric='euclidean', k_neighbors=1):
    """Find nearest neighbors for all source points from a set of candidate points

    Args:
        src_points (np.array): Numpy array containing x and y coordinates of each source point.
        candidates (np.array): Numpy array containing x and y coordinates of each potential destination point.
        metric (str, optional): The measure of distance to use to calculate nearest neighbors. Defaults to 'euclidean'.
        k_neighbors (int, optional): Number of nearest neighbors to find. Defaults to 1.

    Returns:
        closest (np.array): Numpy array of indices of closest candidate to each source point.
        closest_dict (np.array): Numpy array of closest distances between source point and closest candidate point.
    """
    from sklearn.neighbors import BallTree
    import numpy as np

    # Create tree from the candidate points
    tree = BallTree(candidates, leaf_size=15, metric=metric)

    # Find closest points and distances
    distances, indices = tree.query(src_points, k=k_neighbors)

    # Transpose to get distances and indices into arrays
    distances = distances.transpose()
    indices = indices.transpose()

    # Get closest indices and distances (i.e. array at index 0)
    # note: for the second closest points, you would take index 1, etc.
    closest = indices[0]
    closest_dist = distances[0]

    # Return indices and distances
    return (closest, closest_dist)


def nearest_neighbor(left_gdf, right_gdf, metric="euclidean", k_neighbors=1, return_dist=False):
    """Find the nearest neighbor in right_gdf for each point in left_gdf and return the distance between them.

    Args:
        left_gdf (geopandas.GeoDataFrame): GeoDataFrame containing origin locations. This assumes your x and y coordinates are in feet.
        right_gdf (geopandas.GeoDataFrame): GeoDataFrame containing potential destination locations. This assumes your x and y coordinates are in feet.
        metric (str, optional): The measure of distance to use to calculate nearest neighbors. Defaults to "euclidean".
        k_neighbors (int, optional): Number of nearest neighbors to find. Defaults to 1.
        return_dist (bool, optional): A flag indicating whether distances should be returned. Defaults to False.

    Returns:
        closest_points (geopandas.GeoDataFrame): Closest destination locations from right_gdf to each origin location in left_gdf.
    """

    import numpy as np

    #For each point in left_gdf, find closest point in right GeoDataFrame and return them.

    left_geom_col = left_gdf.geometry.name
    right_geom_col = right_gdf.geometry.name

    # Ensure that index in right gdf is formed of sequential numbers
    right = right_gdf.copy().reset_index(drop=True)
    
    if metric == "euclidean":
        # Parse coordinates from points and insert them into a numpy array as FEET
        left_measure = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x, geom.y)).to_list())
        right_measure = np.array(right[right_geom_col].apply(lambda geom: (geom.x, geom.y)).to_list())
    elif metric == "haversine":
    # Parse coordinates from points and insert them into a numpy array as RADIANS
        left_radians = np.array(left_gdf[left_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())
        right_radians = np.array(right[right_geom_col].apply(lambda geom: (geom.x * np.pi / 180, geom.y * np.pi / 180)).to_list())

    
    # Find the nearest points
    # -----------------------
    # closest ==> index in right_gdf that corresponds to the closest point
    # dist ==> distance between the nearest neighbors (in meters)

    closest, dist = get_nearest(src_points=left_measure, candidates=right_measure, metric=metric, k_neighbors=k_neighbors)

    # Return points from right GeoDataFrame that are closest to points in left GeoDataFrame
    closest_points = right.loc[closest]

    # Ensure that the index corresponds the one in left_gdf
    closest_points = closest_points.reset_index(drop=True)

    # Add distance if requested
    if return_dist:
        if metric == "euclidean":
            closest_points['distance'] = dist
        elif metric == "haversine":
            # Convert to miles from radians
            earth_radius = 3,958.7558657  # miles
            closest_points['distance'] = dist * earth_radius

    # We should have exactly the same number of closest_points as we have origin locations
    print("# of closest points:", len(closest_points), '==', "# of origin locations:", len(left_gdf))

    # Rename the geometry of closest stores gdf so that we can easily identify it
    closest_points = closest_points.rename(columns={'geometry': 'closest_poi_geom'})
    
    # Merge the datasets by index (for this, it is good to use '.join()' -function)
    left_gdf = left_gdf.join(closest_points)
    
    return closest_points