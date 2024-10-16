"""
File: reader.py
Author: Djazy Faradj
Created: 09-10-2024
Last modified: 16-10-2024
Description: Reader.py is a script which takes in an image of a qr code (for now, unaltered, 'perfect' qr image), manipulates it a little to then
read each pixel of the code and automatically adapts to varying image sizes as it first calls a funciton CalculateCellSize() in which it will determine the size of
each cell inside that qr code image. From there, it will read the qr code line by line and will then be processed by the QrRead() function.
"""

from qrcode import QrCode       # Contains anything related to qrCodes (both reading and writing)
from settings import *          # Contains changeable settings (i.e. qrcode images directory)
from debug import *              # Used by me for debugging
from PIL import Image           # Used to process QR Code image
from PIL import ImageOps        # Specific function used to better detect QR Code borders

def LoadQRImage(name, extension) -> Image:
    with Image.open(qrCodeFolder + name + "." + extension) as img: # Creates an Image instance from qr code image and loads it as "im"
        newImg = Image.new("L", img.size, "WHITE") # Creates an image based on the one provided, removes alpha channel and turns it into white
        newImg.paste(img, (0, 0), img)
        img = newImg
        invertImg = ImageOps.invert(img) # Invert colors to detect the white->black borders
        img = img.crop(invertImg.getbbox()) # Use those black borders detection to crop the qrCode image to only see code
        return img

def main():
    img = LoadQRImage("big_qr_code", "png")
    qr = QrCode(img)
    qr.Read()
    print(qr) 
    #VisualizeQRCode(qr)
    #VisualizeMaskedQRCode(qr)

main()