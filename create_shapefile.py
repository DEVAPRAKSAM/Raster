import geopandas as gpd
from shapely.geometry import Polygon

# 🔹 Define a simple square polygon
polygon = Polygon([
    (78.0, 12.0), (78.5, 12.0), (78.5, 12.5), (78.0, 12.5), (78.0, 12.0)
])

# 🔹 Create a GeoDataFrame
gdf = gpd.GeoDataFrame({"geometry": [polygon]}, crs="EPSG:4326")

# 🔹 Save as Shapefile
shapefile_path = "data/your_boundary.shp"
gdf.to_file(shapefile_path)

print("✅ Shapefile created successfully at:", shapefile_path)
