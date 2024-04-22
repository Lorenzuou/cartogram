#bin/bash
rm image*

export REGION_SIZE=10
export RESIZE_HEIGHT=500
export RESIZE_WIDTH=500
export IMAGE_NAME="girl"

python3 code_gray.py 

cartogram -p image.json

python3 populate_density.py 

cartogram -ig image_processedmap.json -a image_updated_data.csv 

convert invproj.eps grid.png

python3 rewrite_map.py 