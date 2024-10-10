"""
File: reader.py
Author: Djazy Faradj
Created: 09-10-2024
Last modified: 09-10-2024
Description: Reader.py is a script which takes in an image of a qr code (for now, unaltered, 'perfect' qr image), manipulates it a little as to remove unwanted borders.
It then reads each pixel of this code and automatically adapts to varying image sizes as it first calls a funciton CalculateCellSize() in which it will determine the size of
each cell inside that qr code image. From there, it will read the qr code line by line and will then be processed by the QrRead() function.
"""

import numpy as np
from PIL import Image
from PIL import ImageOps

qrCodeFolder = "sample_qr_codes/"

def LoadQRImage(name, extension):
    with Image.open(qrCodeFolder + name + "." + extension) as im: # Creates an Image instance from qr code image and loads it as "im"
        im = im.convert("L") # Convert qr code image to grayscale
        invertIm = ImageOps.invert(im) # Invert colors to detect the white->black borders
        im = im.crop(invertIm.getbbox()) # Use those black borders detection to crop the qrCode image to only see code
        return np.asarray(im.getdata()) # Convert image into a np array

def main():
    im_data = LoadQRImage("test_black_strip", "png")
    print(im_data)

   

main()