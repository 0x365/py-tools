from PIL import Image

width = 33353
height = 10000

img = Image.new(mode="RGB", size=(width,height))
img.save("big_file.tif")