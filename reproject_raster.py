import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# File paths
input_raster = "results/clipped_raster.tif"
reprojected_output = "results/reprojected_raster.tif"

# Target CRS
target_crs = "EPSG:3857"

# Open the raster
with rasterio.open(input_raster) as src:
    transform, width, height = calculate_default_transform(src.crs, target_crs, src.width, src.height, *src.bounds)
    new_meta = src.meta.copy()
    new_meta.update({"crs": target_crs, "transform": transform, "width": width, "height": height})

    # Reproject and save
    with rasterio.open(reprojected_output, "w", **new_meta) as dst:
        for i in range(1, src.count + 1):
            reproject(source=rasterio.band(src, i), destination=rasterio.band(dst, i),
                      src_transform=src.transform, src_crs=src.crs, dst_transform=transform,
                      dst_crs=target_crs, resampling=Resampling.nearest)

print("✅ Raster Reprojected! Saved as:", reprojected_output)
