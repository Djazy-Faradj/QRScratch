# QR Code Reader (Work in Progress)

I’m creating this QR code reader as a personal challenge, deliberately avoiding the use of any external QR code libraries to make the project more challenging and fulfilling. Instead, I’m using the Pillow library to handle image processing and reading the QR code manually by analyzing its structure and data.

## Features
* **Image Input:** Takes in a QR code image (currently a 'perfect' QR image).
* **Image Processing:** Uses the Pillow library to preprocess the image, such as cropping, resizing, and converting it to an appropriate format.
* **QR Code Analysis:**
	* Detects and processes QR code information such as:
		* QR code version
		* Error correction level
		* Masking pattern
	* Analyzes format strips and data cells.
* **Data Extraction:** Reads the binary data encoded in the QR code image.

## How It Works
1. **Image Loading:** The QR code image is loaded and preprocessed (cropped and resized to ensure the correct dimensions).
2. **QR Code Version Detection:** The program approximates the size of each cell within the QR code to determine its version (ranging from version 1 to 40).
3. **Data Reading:** After processing the image, it reads each individual pixel to extract the QR code's binary data, storing it in a structured array.
4. **Error Correction & Masking:** The error correction level and mask pattern are identified through the format strip, allowing further interpretation of the QR code.

## Libraries Used
* **Pillow:** For image manipulation (cropping, resizing, inverting, etc.).
* **NumPy:** For efficient handling and manipulation of pixel data.

## Current Limitations
* Only works with 'perfect' QR code images (no real-world distortions, noise, or blurring).
* Still in development: Features like handling error correction and real-world image distortions are planned for the future.

## Installation
To install the necessary dependencies, run:

``` pip install pillow numpy matplotlib ```

## Usage
You can run the script by executing:
```python  
python reader.py
```
It will load a sample QR code image (```sample_qr_codes/```) and output the extracted data along with some QR code information (version, error correction level, and mask pattern).

## Special Thanks
This project could not have been possible if not for the incredible and extensive guide about QR Codes made by [Thonky](https://www.thonky.com/qr-code-tutorial/). Credits are also to [Veritasium's amazing video](https://www.youtube.com/watch?v=w5ebcowAJD8&t=1390s) regarding QR Codes which sparked the idea of making this project.

---
