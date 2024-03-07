from PIL import Image
import sys

image_file = sys.argv[1]

Image.MAX_IMAGE_PIXELS = None

im = Image.open(image_file)

im.show()
