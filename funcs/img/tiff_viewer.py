from PIL import Image

Image.MAX_IMAGE_PIXELS = None

im = Image.open('image1.tif')

im.show()
