import matplotlib.pyplot as plt
import numpy as np


def VisualizeQRCode(qr): # For testing purposes, uses matplotlib to visualize qrCode data and generate it to be comparable to origin image.
    N = qr.length
    Z = qr.qrData

    G = np.zeros((N,N,3))

    G[Z>0.5] = [0,0,0] # Sets RBG values to 0 so its black, vice-versa for white pixels..
    G[Z<0.5] = [1,1,1]

    plt.imshow(G,interpolation='nearest')
    plt.show()
    
def VisualizeMaskedQRCode(qr): # For testing purposes, uses matplotlib to visualize qrCode data and generate it to be comparable to origin image.
    N = qr.length
    Z = qr.masked_qr_data

    G = np.zeros((N,N,3))

    G[Z>0.5] = [0,0,0] # Sets RBG values to 0 so its black, vice-versa for white pixels..
    G[Z<0.5] = [1,1,1]

    plt.imshow(G,interpolation='nearest')
    plt.show()