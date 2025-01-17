from constant import *
from math import sqrt
import numpy as np
from PIL import Image

class QrCode:
    version = None # FindVersion() will automatically determine and find the qrCode's version (1(21x21), 2(25x25), 3(29x29), 4(33x33), 10(57x57), 25(117x117), 40(177x177))
    cellSize = None # Same than version except find cell size in pixels
    length = None # QR code length in cells
    qrData = None # Array of size MxN containing the 1s and 0s of the qr code
    raw_data = [] # Actual data bits of the relevant qr code info
    masked_qr_data = None # Array of size MxN containing the 1s and 0s of the qr code following its masking
    blacklisted_coordinates = [] # Array containing the (x,y) coordinates of the non-data values of qr code (i.e. format and version information)
    formatStrip = []
    errorCorrectionLevel = None # String value telling the qr code's error correction level ('Low', 'Medium', 'Quartile', 'High')
    maskPattern = None # Integer value which represents a specific masking template for the qr code

    def __init__(self, img=None, dataType=None, data=None): # QrCode class constructor # Read() will require the 'img' parameter # Write() will require the 'type' and 'data'
        self.img = img
        self.dataType = dataType
        self.data = data
 
    def __str__(self):
        return f'QR Code Version {self.version} | Size: {self.length}x{self.length}\nError Correction Level: {self.errorCorrectionLevel} | Mask pattern: {self.maskPattern}' # Human readable version of qr code class, telling the version
    
    def Write(self):
        pass

    def Read(self): # Calling this function will do all the steps that reads in a QR Code image and outputs a value (returns a string)
        self.imgData = np.asarray(self.img.getdata()) # Convert image into a np array
        self.CellSizeApprox()
        self.FindVersion() # Find version from cell size approx.
        self.FindCellSize() # Find real cell size value
        
        self.length = QR_CODE_LENGTH_BY_VERSION.get(self.version)

        self.ScanQrData()
        self.ReadFormatStrip()
        self.GenerateBlacklist() 
        self.ApplyMask()
        self.ScanRawData()

    def CellSizeApprox(self): # Approximates cell size to first determine qr code version
        for i in range(len(self.imgData)): # Goes over first row of QR code, stops when a pixel is white and then divides the pixel in which it is by 7 to determine cell size
            if self.imgData[i] >= 255:
                self.cellSize = i/7 #i+.23
                break
    def FindVersion(self): # Finds the version of the qr code
        if (QR_CODE_VERSION_BY_LENGTH.get(int(sqrt(len(self.imgData)) / self.cellSize))) == None:
            self.version = QR_CODE_VERSION_BY_LENGTH.get(round(sqrt(len(self.imgData)) / self.cellSize)) # Tries to round the calculated length and checks if belongs to version in dictionary, if not, cast it to int instead
        else:
            self.version = QR_CODE_VERSION_BY_LENGTH.get(int(sqrt(len(self.imgData)) / self.cellSize))
    def FindCellSize(self): # Finds real cell size in pixels
        self.cellSize = (sqrt(len(self.imgData))/QR_CODE_LENGTH_BY_VERSION.get(self.version))          
    
    def ScanQrData(self):
        wpercent = (self.length / float(self.img.size[0])) 
        hsize = int((float(self.img.size[1]) * float(wpercent)))
        self.img = self.img.resize((self.length, hsize), Image.Resampling.NEAREST) # Resizes qr image to appropriate resolution given qr version 
        self.imgData = np.asarray(self.img.getdata()) # Converts resized image into a np array
        self.qrData = np.zeros(self.length*self.length, dtype=int) # Sets the QrCode.qrData to contain an array of length MxN with value 0 for white and 1 for black
        for i in range(len(self.imgData)):
            if self.imgData[i] > WHITE_THRESHOLD: self.qrData[i] = 0 # Checks WHITE_THRESHOLD to determine whether to assign it as black or white value
            else: self.qrData[i] = 1
        self.qrData.shape = (self.length, self.length) # Organizes the data arrays into qrData[row][column] coordinate value
    
    def ReadFormatStrip(self): # Reads raw format strip which will be sent to formatStripCorrection() 
        self.formatStrip.extend(self.qrData[8][0:6].tolist())
        self.formatStrip.extend(self.qrData[8][7:9].tolist())
        self.qrData = self.qrData.swapaxes(0, 1)
        self.formatStrip.append(self.qrData[8][7].item())
        self.formatStrip.extend(self.qrData[8][0:6].tolist()[::-1]) # 
        self.qrData = self.qrData.swapaxes(0, 1)
        self.formatStrip = tuple(self.formatStrip)
        self.FormatStripCorrection()
    def FormatStripCorrection(self): # 11111 0110101010 
        # Compute Hamming Distance of Raw Format Strip# Using a loop 
        hamming_distances = []
        for sequence in VALID_FORMAT_BIT_SEQUENCES:
            hamming_dist = 0
            for a, b in zip(self.formatStrip, tuple(map(int, sequence))): 
                if a != b: hamming_dist += 1 # bitwise XOR between valid format sequence and raw format strip
            hamming_distances.append(hamming_dist)
        valid_sequence_index = hamming_distances.index(min(hamming_distances))
        self.formatStrip = tuple(map(int, VALID_FORMAT_BIT_SEQUENCES[valid_sequence_index]))
        # After correcting format strip, then assign an error correction level and mask 
        self.errorCorrectionLevel = ERROR_CORRECTION_LEVEL.get(self.formatStrip[0:2])
        self.maskPattern = MASK_TEMPLATE.get(self.formatStrip[2:5])

    def GenerateBlacklist(self): # Will generate a blacklist of coordinates which contains non-data bits from qr code so that can be omitted when reading
        ### THIS SECTION TAKES CARE OF ALIGNMENT PATTERNS (Version 2 and above) ###
        if self.version > 1:
            minimum = min(ALIGNMENT_PATTERN_LOCATIONS.get(self.version))
            maximum = max(ALIGNMENT_PATTERN_LOCATIONS.get(self.version))
            alignment_pattern_locations = (
                [(a, b) for idx, a in enumerate(ALIGNMENT_PATTERN_LOCATIONS.get(self.version)) for b in ALIGNMENT_PATTERN_LOCATIONS.get(self.version)[idx + 1:]] 
                + [(b, a) for idx, a in enumerate(ALIGNMENT_PATTERN_LOCATIONS.get(self.version)) for b in ALIGNMENT_PATTERN_LOCATIONS.get(self.version)[idx + 1:]]
                ) # Gets all the possible pair combinations possible
            for coord in ALIGNMENT_PATTERN_LOCATIONS.get(self.version):
                alignment_pattern_locations.append((coord, coord))
            alignment_pattern_locations.append((maximum, maximum))
            # Removes the alignment patterns that are overlapping the finder patterns
            alignment_pattern_locations.remove((minimum, minimum))
            alignment_pattern_locations.remove((minimum, maximum))
            alignment_pattern_locations.remove((maximum, minimum))

            # Get the coordinates of the cells forming the alignment patterns
            for location in alignment_pattern_locations:
                cell_coordinates = []
                center_row = location[0]
                center_col = location[1]
                # Loop through the range -2 to 2 relative to the center point
                for row_offset in range(-2, 3):
                    for col_offset in range(-2, 3):
                        # Calculate the actual row and column for each point
                        row = center_row + row_offset
                        col = center_col + col_offset
                        cell_coordinates.append((row, col))
                self.blacklisted_coordinates += cell_coordinates # Add alignment pattern coordinates to blacklist

        ### THIS SECTION TAKES CARE OF TIMER PATTERNS ###
        for col_pos in range(8, self.length-8):                                     # Horizontal timing pattern
            self.blacklisted_coordinates.append((6, col_pos))
        for row_pos in range(8, self.length-8):                                     # Vertical timing pattern
            self.blacklisted_coordinates.append((row_pos, 6))
        
        ### THIS SECTION TAKES CARE OF FINDER PATTERNS AND SEPARATORS AND FORMAT STRIP AND DARK MODULE ###
        finder_pattern_locations = [(3, 3), (self.length-4, 3), (3, self.length-4)]   # Top-left, Bottom-left, Top-right
        for location in finder_pattern_locations:
            cell_coordinates = []
            center_row = location[0]
            center_col = location[1]
            if location == (3, 3):                                                  # Top-left
                # Loop through the range -2 to 2 relative to the center point
                for row_offset in range(-3, 6):                                     # The extra offset takes care of the separators
                    for col_offset in range(-3, 6):
                        # Calculate the actual row and column for each point
                        row = center_row + row_offset
                        col = center_col + col_offset
                        cell_coordinates.append((row, col))
                self.blacklisted_coordinates += cell_coordinates                     # Add alignment pattern coordinates to blacklist
            elif location == (self.length-4, 3):                                    # Bottom-left
                # Loop through the range -2 to 2 relative to the center point
                for row_offset in range(-4, 4):
                    for col_offset in range(-3, 6):
                        # Calculate the actual row and column for each point
                        row = center_row + row_offset
                        col = center_col + col_offset
                        cell_coordinates.append((row, col))
                self.blacklisted_coordinates += cell_coordinates                     # Add alignment pattern coordinates to blacklist
            elif location == (3, self.length-4):                                    # Top-right
                # Loop through the range -2 to 2 relative to the center point
                for row_offset in range(-3, 6):
                    for col_offset in range(-4, 4):
                        # Calculate the actual row and column for each point
                        row = center_row + row_offset
                        col = center_col + col_offset
                        cell_coordinates.append((row, col))
                self.blacklisted_coordinates += cell_coordinates                     # Add alignment pattern coordinates to blacklist

        self.blacklisted_coordinates = list(set(self.blacklisted_coordinates))

    def ApplyMask(self): # Applies the mask defined in the format strip to the qr code
        self.masked_qr_data = self.qrData.copy()

        if self.maskPattern == Mask.TEMPLATE0:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (row + col)%2 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE1:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if row % 2 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE2:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if col % 3 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE3:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (row + col)%3 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE4:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (row/2 + col/3)%2 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE5:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (row*col)%2 + (row*col)%3 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE6:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (((row*col)%3)+(row*col))%2 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2
        elif self.maskPattern == Mask.TEMPLATE7:
            for row, col in np.ndindex(self.masked_qr_data.shape):
                if (row, col) in self.blacklisted_coordinates: continue
                if (((row*col)%3)+row+col)%2 == 0: self.masked_qr_data[row, col] = (self.masked_qr_data[row, col] + 1) % 2

    def ScanRawData(self):
        starting_point = [self.length-1, self.length-1] # Bottom left corner
        while starting_point[1] >= 1:
            for row_offset in range(0, self.length):    # Upward scanning
                for col_offset in range(0, 2):
                    if (starting_point[0]-row_offset, starting_point[1]-col_offset) not in self.blacklisted_coordinates:
                        self.raw_data.append(self.masked_qr_data[starting_point[0] - row_offset][starting_point[1] - col_offset].item())
            starting_point[0] = 0
            starting_point[1] -= 2 
            if starting_point[1] == 6: starting_point[1] -= 1 # This condition skips the timing pattern column to avoid reading it
            for row_offset in range(0, self.length):    # Downward scanning
                for col_offset in range(0, 2):
                    if (starting_point[0]+row_offset, starting_point[1]-col_offset) not in self.blacklisted_coordinates:
                        self.raw_data.append(self.masked_qr_data[starting_point[0] + row_offset][starting_point[1] - col_offset].item())
            starting_point[0] = self.length-1
            starting_point[1] -= 2
        print(self.raw_data)
        print(len(self.raw_data))

    