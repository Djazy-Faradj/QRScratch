from enum import Enum

WHITE_THRESHOLD = 200 # Tells the program above what value would a pixel be considered "white"

# Assigns the qr code's version to its cell length and vice-versa
QR_CODE_VERSION_BY_LENGTH = {21: 1, 25: 2, 29: 3, 33: 4, 37: 5, 41: 6, 45: 7, 49: 8, 53: 9, 57: 10,                     # Version 1-10
                              61: 11, 65: 12, 69: 13, 73: 14, 77: 15, 81: 16, 85: 17, 89: 18, 93: 19, 97: 20,           # Version 11-20
                              101: 21, 105: 22, 109: 23, 113: 24, 117: 25, 121: 26, 125: 27, 129: 28, 133: 29, 137: 30, # Version 21-30
                              141: 31, 145: 32, 149: 33, 153: 34, 157: 35, 161: 36, 165: 37, 169: 38, 173: 39, 177: 40} # Version 31-40

QR_CODE_LENGTH_BY_VERSION = {1: 21, 2: 25, 3: 29, 4: 33, 5: 37, 6: 41, 7: 45, 8: 49, 9: 53, 10: 57,                     # Version 1-10
                             11: 61, 12: 65, 13: 69, 14: 73, 15: 77, 16: 81, 17: 85, 18: 89, 19: 93, 20: 97,            # Version 11-20
                             21: 101, 22: 105, 23: 109, 24: 113, 25: 117, 26: 121, 27: 125, 28: 129, 29: 133, 30: 137,  # Version 21-30
                             31: 141, 32: 145, 33: 149, 34: 153, 35: 157, 36: 161, 37: 165, 38: 169, 39: 173, 40: 177}  # Version 31-40

# *LOOK UP TABLE* (For error correction of format strip using hamming distance) *See "look up table for error correction format strip.PNG" in /references
VALID_FORMAT_BIT_SEQUENCES = [("111011111000100"), ("111001011110011"), ("111110110101010"), ("111100010011101"), ("110011000101111"),
                              ("110001100011000"), ("110110001000001"), ("110100101110110"), ("101010000010010"), ("101000100100101"),
                              ("101111001111100"), ("101101101001011"), ("100010111111001"), ("100000011001110"), ("100111110010111"),
                              ("100101010100000"), ("011010101011111"), ("011000001101000"), ("011111100110001"), ("011101000000110"),
                              ("010010010110100"), ("010000110000011"), ("010111011011010"), ("010101111101101"), ("001011010001001"),
                              ("001001110111110"), ("001110011100111"), ("001100111010000"), ("000011101100010"), ("000001001010101"), 
                              ("000110100001100"), ("000100000111011")]

# Enum of Mask templates for readability purposes
class Mask(Enum):
    TEMPLATE0 = 0
    TEMPLATE1 = 1
    TEMPLATE2 = 2
    TEMPLATE3 = 3
    TEMPLATE4 = 4
    TEMPLATE5 = 5
    TEMPLATE6 = 6
    TEMPLATE7 = 7

# Assigns format strip's first two values to an error correction level
ERROR_CORRECTION_LEVEL = {(1, 1) : 'Low', (1, 0) : 'Medium', (0, 1) : 'Quartile', (0, 0) : 'High'}

# Assigns format strip's following three values to a Mask Template
MASK_TEMPLATE = {(0, 0, 0) : Mask.TEMPLATE0, (0, 0, 1) : Mask.TEMPLATE1, (0, 1, 0) : Mask.TEMPLATE2, (0, 1, 1) : Mask.TEMPLATE3, (1, 0, 0) : Mask.TEMPLATE4, (1, 0, 1) : Mask.TEMPLATE5, (1, 1, 0) : Mask.TEMPLATE6, (1, 1, 1) : Mask.TEMPLATE7}

