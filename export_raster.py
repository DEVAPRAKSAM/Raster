import rasterio
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# File paths
input_raster = "results/reprojected_raster.tif"
output_png = "results/raster_output.png"
output_jpg = "results/raster_output.jpg"

# Open the raster
with rasterio.open(input_raster) as dataset:
    band1 = dataset.read(1)

    # Normalize pixel values
    band1 = (band1 - band1.min()) / (band1.max() - band1.min()) * 255
    band1 = band1.astype(np.uint8)

    # Save as PNG
    plt.imsave(output_png, band1, cmap="gray")

    # Save as JPEG
    img = Image.fromarray(band1)
    img.save(output_jpg, "JPEG")

print("✅ Raster Exported as PNG and JPEG!")
