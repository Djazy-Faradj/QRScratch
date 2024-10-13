"""
File: reader.py
Author: Djazy Faradj
Created: 09-10-2024
Last modified: 10-10-2024
Description: Reader.py is a script which takes in an image of a qr code (for now, unaltered, 'perfect' qr image), manipulates it a little to then
read each pixel of the code and automatically adapts to varying image sizes as it first calls a funciton CalculateCellSize() in which it will determine the size of
each cell inside that qr code image. From there, it will read the qr code line by line and will then be processed by the QrRead() function.
"""

import numpy as np
from math import sqrt
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from util import *
from constant import *

class QrCode:
    version = None # FindVersion() will automatically determine and find the qrCode's version (1(21x21), 2(25x25), 3(29x29), 4(33x33), 10(57x57), 25(117x117), 40(177x177))
    cellSize = None # Same than version except find cell size in pixels
    cellLength = None
    qrData = None # Array of size MxN containing the 1s and 0s of the qr code
    maskedQrData = None # Array of size MxN containing the 1s and 0s of the qr code following its masking
    blacklistedCoordinates = [] # Array containing the (x,y) coordinates of the non-data values of qr code (i.e. format and version information)
    errorCorrectionLevel = None # String value telling the qr code's error correction level ('Low', 'Medium', 'Quartile', 'High')
    maskPattern = None # Integer value which represents a specific masking template for the qr code

    def __init__(self, im): # QrCode class constructor
        self.im = im
        self.imData = np.asarray(im.getdata()) # Convert image into a np array
        self.CellSizeApprox()
        self.FindVersion() # Find verison from cell size approx.
        self.FindCellSize() # Find real cell size value
        
        self.cellLength = QR_CODE_WIDTH_BY_VERSION.get(self.version)
        self.cellLength = QR_CODE_WIDTH_BY_VERSION.get(self.version)

        self.ScanQrData()
        self.ReadFormatStrip()
        self.ApplyMask()


    def __str__(self):
        return f'QR Code Version {self.version} | Size: {self.cellLength}x{self.cellLength}\nError Correction Level: {self.errorCorrectionLevel} | Mask pattern: {self.maskPattern}' # Human readable version of qr code class, telling the version
    
    def CellSizeApprox(self): # Approximates cell size to first determine qr code version
        for i in range(len(self.imData)): # Goes over first row of QR code, stops when a pixel is white and then divides the pixel in which it is by 7 to determine cell size
            if (self.imData[i] >= 255): 
                self.cellSize = i/7 #i+.23
                break
    def FindVersion(self): # Finds the version of the qr code
        if ((QR_CODE_VERSION_BY_WIDTH.get(int(sqrt(len(self.imData)) / self.cellSize))) == None):
            self.version = QR_CODE_VERSION_BY_WIDTH.get(round(sqrt(len(self.imData)) / self.cellSize)) # Tries to round the calculated width and checks if belongs to version in dictionary, if not, cast it to int instead
        else:
            self.version = QR_CODE_VERSION_BY_WIDTH.get(int(sqrt(len(self.imData)) / self.cellSize))
    def FindCellSize(self): # Finds real cell size in pixels
        self.cellSize = (sqrt(len(self.imData))/QR_CODE_WIDTH_BY_VERSION.get(self.version))          
    
    # Kind of a sequential, step by step approach
    def ScanQrData(self):
        wpercent = (self.cellLength / float(self.im.size[0])) 
        hsize = int((float(self.im.size[1]) * float(wpercent)))
        self.im = self.im.resize((self.cellLength, hsize), Image.Resampling.NEAREST) # Resizes qr image to appropriate resolution given qr version 
        self.imData = np.asarray(self.im.getdata()) # Converts resized image into a np array
        self.qrData = np.zeros(self.cellLength*self.cellLength, dtype=int) # Sets the QrCode.qrData to contain an array of length MxN with value 0 for white and 1 for black
        for i in range(len(self.imData)):
            if (self.imData[i] > WHITE_THRESHOLD): self.qrData[i] = 0 # Checks WHITE_THRESHOLD to determine whether to assign it as black or white value
            else: self.qrData[i] = 1
        self.qrData.shape = (self.cellLength, self.cellLength) # Organizes the data arrays into qrData[row][column] coordinate value
    def ReadFormatStrip(self): # Indicates level of error correction
        self.errorCorrectionLevel = ERROR_CORRECTION_LEVEL.get(tuple(self.qrData[8][0:2]))
        self.maskPattern = MASK_TEMPLATE.get(tuple(self.qrData[8][2:5]))
    def FormatStripCorrection(self):
        pass
    def ApplyMask(self): # Applies the mask defined in the format strip to the qr code
        self.maskedQrData = self.qrData.copy()

        if self.maskPattern == Mask.TEMPLATE0:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (row + col)%2 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE1:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (row)%2 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE2:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (col)%3 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE3:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (row + col)%3 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE4:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (row/2 + col/3)%2 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE5:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (row*col)%2 + (row*col)%3 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE6:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (((row*col)%3)+(row*col))%2 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2
        elif self.maskPattern == Mask.TEMPLATE7:
            for row, col in np.ndindex(self.maskedQrData.shape):
                if (((row*col)%3)+row+col)%2 == 0: self.maskedQrData[row, col] = (self.maskedQrData[row, col] + 1)%2

def LoadQRImage(name, extension):
    with Image.open(qrCodeFolder + name + "." + extension) as im: # Creates an Image instance from qr code image and loads it as "im"
        newIm = Image.new("L", im.size, "WHITE") # Creates an image based on the one provided, removes alpha channel and turns it into white
        newIm.paste(im, (0, 0), im)
        im = newIm
        invertIm = ImageOps.invert(im) # Invert colors to detect the white->black borders
        im = im.crop(invertIm.getbbox()) # Use those black borders detection to crop the qrCode image to only see code
        return im

def main():
    im = LoadQRImage("githublink", "png")
    qr = QrCode(im)
    print(qr)

main()