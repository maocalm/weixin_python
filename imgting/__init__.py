
from PIL import Image

im = Image.open("wmb010.png")
im2 = im.convert('P')
im2.save("optimized.png",optimize=True)