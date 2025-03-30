import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image

# File paths (Update these with your actual files)
input_raster = "data/your_raster.tif"
shapefile_path = "data/your_boundary_fixed.shp"
ndvi_output = "results/ndvi_output.tif"
clipped_output = "results/clipped_raster.tif"
reprojected_output = "results/reprojected_raster.tif"
png_output = "results/raster_output.png"
jpg_output = "results/raster_output.jpg"

# Step 1: Read and Display Raster
with rasterio.open(input_raster) as dataset:
    print("Raster Details:")
    print(f"Width: {dataset.width}, Height: {dataset.height}")
    print(f"Number of Bands: {dataset.count}, CRS: {dataset.crs}")
    band1 = dataset.read(1)
    plt.imshow(band1, cmap="gray")
    plt.colorbar(label="Pixel Value")
    plt.title("Original Raster")
    plt.show()

# Step 2: NDVI Calculation
with rasterio.open(input_raster) as dataset:
    red_band = dataset.read(3).astype(float)
    nir_band = dataset.read(4).astype(float)
    ndvi = (nir_band - red_band) / (nir_band + red_band)

    with rasterio.open(ndvi_output, "w", driver="GTiff", height=ndvi.shape[0], width=ndvi.shape[1],
                       count=1, dtype=ndvi.dtype, crs=dataset.crs, transform=dataset.transform) as dst:
        dst.write(ndvi, 1)
    print("NDVI Calculation Done! Saved as:", ndvi_output)

# Step 3: Clip Raster Using Shapefile
shapefile = gpd.read_file(shapefile_path)
geometry = [shapefile.geometry[0]]
with rasterio.open(input_raster) as src:
    clipped, transform = mask(src, geometry, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"height": clipped.shape[1], "width": clipped.shape[2], "transform": transform})
    with rasterio.open(clipped_output, "w", **out_meta) as dest:
        dest.write(clipped)
print("Raster Clipped! Saved as:", clipped_output)

# Step 4: Reproject Raster
target_crs = "EPSG:3857"
with rasterio.open(clipped_output) as src:
    transform, width, height = calculate_default_transform(src.crs, target_crs, src.width, src.height, *src.bounds)
    new_meta = src.meta.copy()
    new_meta.update({"crs": target_crs, "transform": transform, "width": width, "height": height})
    with rasterio.open(reprojected_output, "w", **new_meta) as dst:
        for i in range(1, src.count + 1):
            reproject(source=rasterio.band(src, i), destination=rasterio.band(dst, i),
                      src_transform=src.transform, src_crs=src.crs, dst_transform=transform,
                      dst_crs=target_crs, resampling=Resampling.nearest)
print("Raster Reprojected! Saved as:", reprojected_output)

# Step 5: Export as PNG and JPEG
with rasterio.open(reprojected_output) as dataset:
    band1 = dataset.read(1)
    band1 = (band1 - band1.min()) / (band1.max() - band1.min()) * 255
    band1 = band1.astype(np.uint8)
    plt.imsave(png_output, band1, cmap="gray")
    img = Image.fromarray(band1)
    img.save(jpg_output, "JPEG")
print("Raster Exported as PNG and JPEG!")
