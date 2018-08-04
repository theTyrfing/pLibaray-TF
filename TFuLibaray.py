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
from tkinter import filedialog
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
from time import time
from math import sqrt
import random

#Import Constants
from TFuConfig import *

#Data Import Functions
#--------------------------------------------------------
#dir dialog function
def pickDirectory():
    dirLocation = Tk()
    dirLocation.directory = filedialog.askdirectory()
    dirString = dirLocation.directory
    dirLocation.destroy()
    return dirString

def pickFile(fExt):
    fLocation = Tk()
    fLocation.filename = filedialog.askopenfilename(initialdir = "/",\
                                                    title = "Select file",\
                                                    filetypes = ((fExt+" files","*."+fExt),/
                                                                 ("all files","*.*")))
    fString = fLocation.filename
    fLocation.destroy()
    return fString

def saveFile(fExt):
    fLocation = Tk()
    fLocation.filename = filedialog.asksaveasfilename(initialdir = "/",\
                                                      title = "Select file",\
                                                      iletypes = ((fExt+" files","*."+fExt),/
                                                                  ("all files","*.*")))
    fString = fLocation.filename
    fLocation.destroy()
    return fString

#importing photos
def loadPic(pathString):
    directories = [d for d in os.listdir(pathString) 
                   if os.path.isdir(os.path.join(pathString, d))]
    labels = []
    images = []
    for d in directories:
        #label is extracted from the name of sub directory
        label_directory = os.path.join(pathString, d)
        file_names = [os.path.join(label_directory, f) 
                      for f in os.listdir(label_directory) 
                      if f.endswith(iFile)]
        #reads file
        for f in file_names:
            images.append(io.imread(f, as_gray = True))
            labels.append(int(d))

    #Resize Image for processing
    images = [transform.resize(image, (iSize, iSize)) for image in images]
    
    return images, labels

#Test Functions
#--------------------------------------------------------

def dImages(images, labels):
    
    # Get the unique labels 
    unique_labels = set(labels)

    # Initialize the figure
    plt.figure(figsize=(15, 15))

    # Set a counter
    i = 1

    # For each unique label,
    for label in unique_labels:
        # You pick the first image for each label
        image = images[labels.index(label)]
        # Define 64 subplots 
        plt.subplot(8, 8, i)
        # Don't include axes
        plt.axis('off')
        # Add a title to each subplot 
        plt.title("Label {0} ({1})".format(label, labels.count(label)))
        # Add 1 to the counter
        i += 1
        # And you plot this first image 
        plt.imshow(image)
    
    # Show the plot
    plt.show()

#Deep Learning Functions
#--------------------------------------------------------

def testPrint(net):
    print("images_flat: ", net.images_flat)
    print("logits: ", net.logits)
    print("loss: ", net.loss)
    print("predicted_labels: ", net.correct_pred)

def testPlot(images28,labels,network):
    # Pick 10 random images
    sample_indexes = random.sample(range(len(images28)), 10)
    sample_images = [images28[i] for i in sample_indexes]
    sample_labels = [labels[i] for i in sample_indexes]

    # Run the "correct_pred" operation
    network.prediction(sample_images)
                        
    # Print the real and predicted labels
    print(sample_labels)
    print(network.predicted)

    # Display the predictions and the ground truth visually.
    fig = plt.figure(figsize=(10, 10))
    for i in range(len(sample_images)):
        truth = sample_labels[i]
        prediction = network.predicted[i]
        plt.subplot(5, 2,1+i)
        plt.axis('off')
        color='green' if truth == prediction else 'red'
        plt.text(40, 10, "Truth:        {0}\nPrediction: {1}".format(truth, prediction), 
            fontsize=12, color=color)
        plt.imshow(sample_images[i],  cmap="gray")

    plt.show()
        

class snNetwork:
    pass
    
    #Initalization functions
    def __init__(self):

        #Generate Seed
        self.seed =round(sqrt(time()))
        tf.set_random_seed(self.seed)

        #Set Placeholders Workspace values
        self.x = tf.placeholder(dtype = tf.float32, shape = [None, iSize, iSize])
        self.y = tf.placeholder(dtype = tf.int32, shape = [None])

    #Configuring tensors & layers
    def configTF(self):
        # Flatten the input data
        self.images_flat = tf.contrib.layers.flatten(self.x)

        # Fully connected layer 
        self.logits = tf.contrib.layers.fully_connected(self.images_flat, nOutput tf.nn.relu)

        # Define a loss function
        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = self.y, 
                                                                    logits = self.logits))
        # Define an optimizer 
        self.train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)

        # Convert logits to label indexes
        self.correct_pred = tf.argmax(self.logits, 1)

        # Define an accuracy metric
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

    #Session function
    def session(self):
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    #Train model
    def training(self, imgDict,labDict):
        self.session()
        for i in range(nEpoch):
            _, accuracy_val = self.sess.run([self.train_op, self.accuracy], feed_dict={self.x: imgDict, self.y: labDict})
            #if i % 10 == 0:
                #print('EPOCH', i)
                #print("Loss: ", self.loss)
            #print('DONE WITH EPOCH')

    #Get prediction
    def prediction(self,sample_images):
        self.predicted = self.sess.run([self.correct_pred], feed_dict={self.x: sample_images})[0]

    #Save Model
    def saveNet(self):
        saver = tf.train.Saver()
        savePath = saveFile("ckpt")
        savePath = saver.save(self.sess,savePath)
