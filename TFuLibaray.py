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
import mnist
import random
import scipy.misc
import math

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
                                                    filetypes = ((fExt+" files","*."+fExt),\
                                                                 ("all files","*.*")))
    fString = fLocation.filename
    fLocation.destroy()
    return fString

def saveFile(fExt):
    fLocation = Tk()
    fLocation.filename = filedialog.asksaveasfilename(initialdir = "/",\
                                                      title = "Select file",\
                                                      filetypes = ((fExt+" files","*."+fExt),\
                                                                  ("all files","*.*")))
    fString = fLocation.filename
    fLocation.destroy()
    return fString

#importing from MNIST
def loadMTrain():
    images = mnist.train_images()
    labels = mnist.train_labels()
    #images = images.reshape((images.shape[0], images.shape[1] * images.shape[2]))
    return images, labels

def loadMTest():
    images = mnist.test_images()
    labels = mnist.test_labels()
    #images = images.reshape((images.shape[0], images.shape[1] * images.shape[2]))
    return images, labels

def batcher(images,labels,bNum):
    if bNum == -1:
        return images, labels
    if isinstance(images,list):
        num = len(images)/bNum
        nImages = np.asarray(images)
        nLabels = np.asarray(labels)
    else:
        num = images.shape[0]/bNum
        nImages = images
        nLabels = labels
    print(num)
    nImages = np.split(nImages,num)
    nLabels = np.split(nLabels,num)
    return nImages, nLabels    

#importing photos
def loadPic():
    
    pathString = pickDirectory()
    
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

def testRun(images28,labels,network):
    network.chkAccuracy(images28,labels)

def testPlot(images28,labels,network):
    #Check Accuracy
    network.chkAccuracy(images28,labels)
    
    # Pick 10 random images
    sample_indexes = random.sample(range(len(images28)), 10)
    sample_images = [images28[i] for i in sample_indexes]
    sample_labels = [labels[i] for i in sample_indexes]

    # Run the "correct_pred" operation
    network.prediction(sample_images,sample_labels)
                        
    # Print the real and predicted labels
    print(sample_labels)
    print(network.predicted)
    network.chkAccuracy(sample_images,sample_labels)

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
        self.y_ = tf.to_int64(self.y)

    #Configuring tensors & layers
    def configTF(self):
        # Flatten the input data
        self.images_flat = tf.contrib.layers.flatten(self.x)

        # Fully connected layer - determining logits (Weights & Bias)
        if cType == 0:
            self.logits = tf.contrib.layers.fully_connected(self.images_flat, nOutput, tf.nn.relu)
        elif cType == 1:
            self.logits = inference(self.images_flat,hiddenU1,hiddenU2)
        else:
            self.logits = tf.contrib.layers.fully_connected(self.images_flat, nOutput, tf.nn.relu)
        
        # Define a loss function
        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = tf.to_int64(self.y), 
                                                                    logits = self.logits))
        # Define an optimizer 
        if cOptimizer == "Adam":
            self.train_op = tf.train.AdamOptimizer(learning_rate=learnRate).minimize(self.loss)
        else:
            self.train_op = tf.train.GradientDescentOptimizer(learning_rate=learnRate).minimize(self.loss)
            
        # Convert logits to label indexes
        self.correct_pred = tf.argmax(self.logits, 1)

        # %Accuracy prediction
        self.correct_preAcc = tf.equal(tf.argmax(self.logits, 1), self.y_)
        self.accuracyX = tf.reduce_mean(tf.cast(self.correct_preAcc, tf.float32))

        # Define an accuracy metric
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

    #Check accuracy
    def chkAccuracy(self, imgDict,labDict):
        print(str(self.sess.run(self.accuracyX, feed_dict={self.x:imgDict,self.y:labDict}))*100 + "%")
    
    #Session function
    def session(self):
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    #Train model
    def training(self, imgDict,labDict):
        self.session()
        print("Start Training")

        #Temp batches
        bImages, bLabel = batcher(imgDict,labDict,batchSize)
        if batchSize == -1:
            nTime = nEpoch

            for i in range(nTime):
                _, accuracy_val = self.sess.run([self.train_op, self.accuracy], feed_dict={self.x: bImages, self.y: bLabel})
                if i*100/nTime % 10 == 0:
                    print("Training at " + str(100*i/nTime) + "%")
                    print("Loss: %.2f" % accuracy_val)
        else:
            nTime = len(bLabel)
        
            for i in range(nTime):
                _, accuracy_val = self.sess.run([self.train_op, self.accuracy], feed_dict={self.x: bImages[i], self.y: bLabel[i]})
                if i*100/nTime % 10 == 0:
                    print("Training at " + str(100*i/nTime) + "%")
                    print("Loss: %.2f" % accuracy_val)

        print("Training at " + str(100*i/nTime) + "%")
        print("Loss: %.2f" % accuracy_val)
        print('Done with Training.')
        
    #Get prediction
    def prediction(self,sample_images,sample_labels):
            self.predicted = self.sess.run([self.correct_pred], feed_dict={self.x: sample_images})[0]

    #Save Model
    def saveNet(self):
        saver = tf.train.Saver()
        savePath = saveFile("ckpt")
        savePath = saver.save(self.sess,savePath)

def inference(images, hidden1_units, hidden2_units):
  """Build the MNIST model up to where it may be used for inference.
  Args:
    images: Images placeholder, from inputs().
    hidden1_units: Size of the first hidden layer.
    hidden2_units: Size of the second hidden layer.
  Returns:
    softmax_linear: Output tensor with the computed logits.
  """
  # Hidden 1
  with tf.name_scope('hidden1'):
    weights = tf.Variable(
        tf.truncated_normal([IMAGE_PIXELS, hidden1_units],
                            stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))),
        name='weights')
    biases = tf.Variable(tf.zeros([hidden1_units]),
                         name='biases')
    hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)
  # Hidden 2
  with tf.name_scope('hidden2'):
    weights = tf.Variable(
        tf.truncated_normal([hidden1_units, hidden2_units],
                            stddev=1.0 / math.sqrt(float(hidden1_units))),
        name='weights')
    biases = tf.Variable(tf.zeros([hidden2_units]),
                         name='biases')
    hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)
  # Linear
  with tf.name_scope('softmax_linear'):
    weights = tf.Variable(
        tf.truncated_normal([hidden2_units, NUM_CLASSES],
                            stddev=1.0 / math.sqrt(float(hidden2_units))),
        name='weights')
    biases = tf.Variable(tf.zeros([NUM_CLASSES]),
                         name='biases')
    logits = tf.matmul(hidden2, weights) + biases
  return logits
