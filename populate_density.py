import rasterio
import numpy as np
import pandas as pd
import os 
import cv2
IMAGE_NAME = os.environ.get("IMAGE_NAME", "gray_resized.jpg")

REGION_SIZE = int(os.environ.get('REGION_SIZE', 10))
# Load the CSV file into a DataFrame
df = pd.read_csv('image_data.csv')
resized_name = IMAGE_NAME + "_resized.jpg"

# Convert the grayscale image to a numpy array
with rasterio.open(resized_name) as src:
    grayscale_array = src.read(1)


# Create a dictionary to store the average grayscale value for each region
region_values = {}
count = 0

print("grayscale_array.shape[1]: ", len(range(0, grayscale_array.shape[1],
                                              REGION_SIZE)))
# Iterate over the numpy array in chunks of region_size
# Define the kernel for the 2D filter
kernel = np.ones((REGION_SIZE, REGION_SIZE), np.float32) / (REGION_SIZE * REGION_SIZE)

# Initialize the dictionary to store the region values
region_values = {}

# Initialize the count for the region name
count = 0

# Iterate over the numpy array in chunks of region_size
for row in range(0, grayscale_array.shape[0], REGION_SIZE):
    for col in range(0, grayscale_array.shape[1], REGION_SIZE):
        # Apply the 2D filter to this region
        region = grayscale_array[row:row+REGION_SIZE, col:col+REGION_SIZE]
        filtered_region = cv2.filter2D(region, -1, kernel)

        # Get the region name from the DataFrame
        region_name = df.loc[count, 'Region Name']
        # Store the filtered region for this region
        region_values[region_name] = filtered_region.mean()
        count += 1

print("count: ", count)

# #normalize region_values
# max_value = max(region_values.values())
# min_value = min(region_values.values())
# for key in region_values:
#     region_values[key] = 1 - (region_values[key] - min_value) / (max_value - min_value)


#edit the csv file 
df['Region Data'] = df['Region Name'].map(region_values)

#save the updated csv file
df.to_csv('image_updated_data.csv', index=False)