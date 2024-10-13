from enum import Enum

# Directory containing the qr code images
qrCodeFolder = "sample_qr_codes/"

WHITE_THRESHOLD = 200 # Tells the program above what value would a pixel be considered "white"

# Assigns the qr code's version to its cell length and vice-versa
QR_CODE_VERSION_BY_LENGTH = {21: 1, 25: 2, 29: 3, 33: 4, 57: 10, 117: 25, 177: 40}
QR_CODE_LENGTH_BY_VERSION = {1: 21, 2: 25, 3: 29, 4: 33, 10: 57, 25: 117, 40: 177}

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

