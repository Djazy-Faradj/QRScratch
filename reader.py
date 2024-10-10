"""
File: reader.py
Author: Djazy Faradj
Created: 09-10-2024
Last modified: 10-10-2024
Description: Reader.py is a script which takes in an image of a qr code (for now, unaltered, 'perfect' qr image), manipulates it a little as to remove unwanted borders.
It then reads each pixel of this code and automatically adapts to varying image sizes as it first calls a funciton CalculateCellSize() in which it will determine the size of
each cell inside that qr code image. From there, it will read the qr code line by line and will then be processed by the QrRead() function.
"""

import numpy as np
from math import sqrt
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from constant import *

qrCodeFolder = "sample_qr_codes/"

class QrCode:
    version = None # FindVersion() will automatically determine and find the qrCode's version (1(21x21), 2(25x25), 3(29x29), 4(33x33), 10(57x57), 25(117x117), 40(177x177))
    cell_size = None # Same than version except find cell size in pixels
    cell_width = None
    cell_height = None
    qrData = None

    def __init__(self, imData): # QrCode class constructor
        self.imData = imData
        self.CellSizeApprox()

        self.FindVersion() # Find verison from cell size approx.
        self.FindCellSize() # Find real cell size value
        self.cell_width = QR_CODE_WIDTH_BY_VERSION.get(self.version)
        self.cell_height = QR_CODE_WIDTH_BY_VERSION.get(self.version)
        np.array()

    def __str__(self):
        return f'QR Code Version {self.version} : Size: {self.cell_width}x{self.cell_height}' # Human readable version of qr code class, telling the version
    
    def CellSizeApprox(self):
        # Cell size approximation
        for i in range(len(self.imData)): # Goes over first row of QR code, stops when a pixel is white and then divides the pixel in which it is by 7 to determine cell size
            if (self.imData[i] >= WHITE_THRESHOLD): 
                self.cell_size = i/7 #i+.23
                break
    def FindVersion(self): # Finds the version of the qr code and sets it to version attribute
        if ((QR_CODE_VERSION_BY_WIDTH.get(int(sqrt(len(self.imData)) / self.cell_size))) == None):
            self.version = QR_CODE_VERSION_BY_WIDTH.get(round(sqrt(len(self.imData)) / self.cell_size)) # Tries to round the calculated width and checks if belongs to version in dictionary, if not, cast it to int instead
        else:
            self.version = QR_CODE_VERSION_BY_WIDTH.get(int(sqrt(len(self.imData)) / self.cell_size))
    def FindCellSize(self): # Returns real cell size in pixels
        self.cell_size = (sqrt(len(self.imData))/QR_CODE_WIDTH_BY_VERSION.get(self.version))

    def ReadQrData(self):
        cell_pixel_length = self.cell_width/sqrt(len(self.imData)) # Assuming square cells 
        
        i = 0 # Value keeping track of which pixel coordinate we are in
        j = 0 # Value keeping track of which cell coordinate we are in
        
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell_values = self.imData[i+(j*cell_pixel_length*self.cell_width):i+(j*cell_pixel_length*self.cell_width)+cell_pixel_length]
                
            

def QrRead(qrCode):
    pass

def LoadQRImage(name, extension):
    with Image.open(qrCodeFolder + name + "." + extension) as im: # Creates an Image instance from qr code image and loads it as "im"
        newIm = Image.new("L", im.size, "WHITE") # Creates an image based on the one provided, removes alpha channel and turns it into white
        newIm.paste(im, (0, 0), im)
        im = newIm
        invertIm = ImageOps.invert(im) # Invert colors to detect the white->black borders
        im = im.crop(invertIm.getbbox()) # Use those black borders detection to crop the qrCode image to only see code
        return np.asarray(im.getdata()) # Convert image into a np array

def main():
    imData = LoadQRImage("githublink", "png")
    qr = QrCode(imData)
    print(qr)

main()