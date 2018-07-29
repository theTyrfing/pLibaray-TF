#Utility Libaray for AI Deep Learning functions
#By Regan Lu
#--------------------------------------------------------
#Uses tensorflow libaray and make special functions for
#importing data and setup layers
#--------------------------------------------------------
#Change Log
#--------------------------------------------------------

#Load Libaries
#--------------------------------------------------------
import tensorflow as tf
import os
from tkinter import *
from skimage import transform
from skimage.color import rgb2gray

#Import Constants
from TFuConstants import *

#Data Import Functions
#--------------------------------------------------------
#file dialog function
def pickDirectory():
    dirLocation = Tk()
    dirLocation.directory = filedialog.askdirectory()
    return dirLocation.directory

#importing photos
def loadPic(pathString):
    directories = [d for d in os.listdir(data_directory) 
                   if os.path.isdir(os.path.join(data_directory, d))]
    labels = []
    images = []
    for d in directories:
        label_directory = os.path.join(data_directory, d)
        file_names = [os.path.join(label_directory, f) 
                      for f in os.listdir(label_directory) 
                      if f.endswith(".ppm")]
        for f in file_names:
            images.append(skimage.data.imread(f))
            labels.append(int(d))
    return images, labels

#Image Processing Functions
#--------------------------------------------------------

def procImages(images):
    print('')
    
