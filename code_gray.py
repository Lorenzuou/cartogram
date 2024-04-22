from PIL import Image
import numpy as np
import rasterio
import json

import os

REGION_SIZE = int(os.environ.get('REGION_SIZE', 10))
RESIZE_HEIGHT = int(os.environ.get('RESIZE_HEIGHT', 500))
RESIZE_WIDTH = int(os.environ.get('RESIZE_WIDTH', 500))

IMAGE_NAME = os.environ.get("IMAGE_NAME", "girl")

print("REGION_SIZE: ", REGION_SIZE)
print("RESIZE_HEIGHT: ", RESIZE_HEIGHT)
print("RESIZE_WIDTH: ", RESIZE_WIDTH)

def convert_to_grayscale(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to grayscale
        gray_img = img.convert('L')
        return gray_img
    
    
# Use the function
gray_image = convert_to_grayscale(IMAGE_NAME + ".jpg")
# Save the grayscale image
gray_image.save('gray.jpg')

gray_image = gray_image.resize((RESIZE_HEIGHT, RESIZE_WIDTH))
resized_name = IMAGE_NAME + "_resized.jpg"
gray_image.save(resized_name)

# Convert the grayscale image to a numpy array
with rasterio.open(resized_name) as src:
    grayscale_array = src.read(1)

# Initialize the GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}
count = 0
#resize image, 100x100
#save image resized 
count = 0
# Iterate over the numpy array in chunks of region_size
for row in range(0, grayscale_array.shape[0], REGION_SIZE):
    for col in range(0, grayscale_array.shape[1], REGION_SIZE):
        # Calculate the average grayscale value in this region
        region = grayscale_array[row:row+REGION_SIZE, col:col+REGION_SIZE]
        avg_value = np.mean(region)

        # Create a polygon for this region
        polygon = {
            "type": "Polygon",
            "coordinates": [[
                [float(col), float(row)],
                [float(col + REGION_SIZE), float(row)],
                [float(col + REGION_SIZE), float(row + REGION_SIZE)],
                [float(col), float(row + REGION_SIZE)],
                [float(col), float(row)]
            ]]
        }

        # Create a feature for this region
        feature = {
            "type": "Feature",
            "geometry": polygon,
            "id": count,
            "properties": {
                "avg_grayscale_value": avg_value,
                "region_name": f"region_{row//REGION_SIZE}_{col//REGION_SIZE}"
            }
        }
        count += 1

        # Add the feature to the GeoJSON
        geojson["features"].append(feature)

# Write the GeoJSON to a file
with open('image.json', 'w') as f:
    json.dump(geojson, f)