from PIL import Image

def tiff_input(image_file):

    Image.MAX_IMAGE_PIXELS = None

    im = Image.open(image_file)

    im.show()
