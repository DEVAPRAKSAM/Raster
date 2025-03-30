import rasterio
import geopandas as gpd
from rasterio.mask import mask

# File paths
input_raster = "data/your_raster.tif"
shapefile_path = "data/your_boundary_fixed.shp"
clipped_output = "results/clipped_raster.tif"

# Load the shapefile
shapefile = gpd.read_file(shapefile_path)

# Open the raster to get its CRS
with rasterio.open(input_raster) as src:
    raster_crs = src.crs

    # 🔹 Reproject shapefile to match raster CRS (if different)
    if shapefile.crs != raster_crs:
        print(f"⚠️ Shapefile is in {shapefile.crs}, reprojecting to {raster_crs}...")
        shapefile = shapefile.to_crs(raster_crs)

    # Extract geometry from the reprojected shapefile
    geometry = [shapefile.geometry[0]]

    # Clip raster using the shapefile geometry
    clipped, transform = mask(src, geometry, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"height": clipped.shape[1], "width": clipped.shape[2], "transform": transform})

    # Save the clipped raster
    with rasterio.open(clipped_output, "w", **out_meta) as dest:
        dest.write(clipped)

print("✅ Raster Clipped Successfully! Saved as:", clipped_output)
