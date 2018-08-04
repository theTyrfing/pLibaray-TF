#import sys
#sys.path.append('C:\Users\Regan\Documents\GitHub\pLibaray-TF')

from TFuLibaray import *

tImage, tLabel = loadMTrain()

#dImages(tImage, tLabel)

test = snNetwork()

print (test.seed)

test.configTF()

testPrint(test)

test.training(tImage,tLabel)

testPlot(tImage,tLabel,test)
