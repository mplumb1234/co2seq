import shapely.geometry
import os
import plotly.graph_objects as go
import geopandas as gpd

def lat_lon_lists_from_df(df):
    lats = []
    lons = []
    for feature in df.geometry:
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            for lat, lon in zip(y, x):
                lats.append(lat)
                lons.append(lon)
            lats.append(None)
            lons.append(None)
    return lats, lons


def load_dfs(path, allowed_extensions=[".shp", ".zip", ".csv", ".gdb"]):
    dfs = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(subdir, file)
            extension = os.path.splitext(file_name)[1]
            if allowed_extensions.count(extension) != 0:
                try:
                    dfs[file] = gpd.read_file(file_name)
                except:
                    raise Exception(f"Error loading dataframes from {path}")
    return dfs

def get_traces_from_dfs(dfs):
    traces = []
    colors = ["red", "yellow", "green", "pink", "orange", "purple"]
    counter = 0
    for df_name, df in dfs.items():
        print(df.head)
        if "geometry" in df:
            if isinstance(df.geometry[0], shapely.geometry.linestring.LineString) \
                    or isinstance(df.geometry[0], shapely.geometry.multilinestring.MultiLineString):
                lats, lons = lat_lon_lists_from_df(df)
                traces.append(go.Scattermapbox(name=df_name, visible="legendonly", lon=lons, lat=lats, mode='lines', line=dict(width=1, color=colors[counter%len(colors)])))
                counter += 1
            elif isinstance(df.geometry[0], shapely.geometry.point.Point):
                df['lon'] = df['geometry'].x
                df['lat'] = df['geometry'].y
                traces.append(go.Scattermapbox(name=df_name, visible="legendonly", lat=df['lat'], lon=df['lon'], marker ={'color': colors[counter%len(colors)], 'size': 5, 'opacity': 0.6}))
                counter += 1
    return traces