#Utility Libaray Constants for AI Deep Learning functions
#By Regan Lu
#--------------------------------------------------------
#Uses tensorflow libaray and make special functions for
#importing data and setup layers
#--------------------------------------------------------
#Change Log
#--------------------------------------------------------

#Constants & Settings

iSize = 28   #Image Size

iFile = ".ppm" #Image Size

nEpoch = 201 #Number of Epochs/Training Loops

nOutput = 62 #Number of Outputs

learnRate = 0.0005 #Learning Rate

batchSize = -1 #Size of Batch, Default = None

cOptimizer = "Adam" #Optimizer choice ("Adam" , "Gradient")

cType = 0 #Evaluation method

IMAGE_PIXELS = iSize * iSize

NUM_CLASSES = nOutput

hiddenU1 = 125

hiddenU2 = 32
