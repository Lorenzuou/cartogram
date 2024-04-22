import subprocess
from PIL import Image
import os 

IMAGE_NAME = os.environ.get('IMAGE_NAME', 'girl')


def remove_white_background(image_path):
    # Open the PNG file
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()
    print("shape: ", img.size)

    new_data = []
    for item in datas:
        # Check if the pixel is white-like
        if item[0] >= 200 and item[1] >= 200 and item[2] >= 200:
            # Set the pixel to transparent
            new_data.append((item[0], item[1], item[2], 0))
        else:
            # Set the pixel to red
            new_data.append((255, 0, 0, item[3]))

    img.putdata(new_data)
    new_image_path = image_path.split('.')[0] + '_no_bg.png'
    img.save(new_image_path, "PNG")


def filter_eps_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start = next(i for i, line in enumerate(lines) if line.strip() == 'n')
    end = next(i for i, line in enumerate(lines[start:], start=start) if 'SLW' in line) + 1

    with open(file_path, 'w') as file:
        for i, line in enumerate(lines):
            if i < start or i >= end:
                file.write(line)



def apply_grid(image_path, grid_path, output_path):
    # Convert the EPS file to PNG
    subprocess.run(['convert', grid_path, 'grid.png'])

    # Remove white background from the grid
    remove_white_background('grid.png')

    # Open the image and the grid
    with Image.open(image_path) as img, Image.open('grid_no_bg.png') as grid:
        #print shape of img 
        # Resize the grid to match the image size
        grid = grid.resize(img.size)
        # img is in grayscale, convert it to RGB for transparency
        img = img.convert('RGB')

        #grid same size as img
        grid = grid.resize(img.size)
        # paste the grid on top of the image
        img.paste(grid, (0, 0), grid)

        # Save the result
        img.save(output_path)


# # Use the function
# filter_eps_file('invproj.eps')

# resized_name = IMAGE_NAME + "_resized.jpg"

# # Use the function
# apply_grid(resized_name, 'invproj.eps', IMAGE_NAME + '_output.jpg')
        

filter_eps_file('assets/invproj.eps')
