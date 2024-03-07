from PIL import Image

Image.MAX_IMAGE_PIXELS = None

big_image = "image_in"
input_format = ".tif"

split_into = 10



im = Image.open(big_image+input_format)
width, height = im.size

for x in range(0, width, round(width/split_into)):
    for y in range(0, height, round(height/split_into)):
        im_cropped = im.crop((x, y, x+(width/split_into), y+(height/split_into)))
        im_cropped.save("./cropped/"+big_image+"_"+str(x)+"x_"+str(y)+"y.tif")
