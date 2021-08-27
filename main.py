import os
from PIL import Image


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def print_hi(name):
    directory = "images"
    # Use a breakpoint in the code line below to debug your script.
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(directory, filename)
            original = Image.open(file_path)
            small_tile = original.resize((16, 16), Image.NEAREST)
            small_tile.save("tiles/" + filename)
            image_rgb = small_tile.convert("RGB")

            for x in range(0, 15):
                for y in range(0, 15):
                    coordinate = x, y
                    print(image_rgb.getpixel(coordinate))

        else:
            continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
