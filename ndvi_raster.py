import rasterio
import numpy as np

# File paths
input_raster = "data/your_raster.tif"
ndvi_output = "results/ndvi_output.tif"

# Open the raster dataset
with rasterio.open(input_raster) as dataset:
    print(f"✅ Raster has {dataset.count} bands")  # Debugging

    # If the raster has only 3 bands, use Red = Band 1 and NIR = Band 3
    red_band = dataset.read(1).astype(float)
    nir_band = dataset.read(3).astype(float) if dataset.count >= 3 else red_band  

    # Calculate NDVI
    ndvi = (nir_band - red_band) / (nir_band + red_band)

    # Save NDVI output
    with rasterio.open(ndvi_output, "w", driver="GTiff", height=ndvi.shape[0], width=ndvi.shape[1],
                       count=1, dtype=ndvi.dtype, crs=dataset.crs, transform=dataset.transform) as dst:
        dst.write(ndvi, 1)

print("✅ NDVI Calculation Done! Saved as:", ndvi_output)
