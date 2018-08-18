#import sys
#sys.path.append('C:\Users\Regan\Documents\GitHub\pLibaray-TF')

from TFuLibaray import *

tImage, tLabel = loadPic()

#testI, testL = loadMTest()

#dImages(tImage, tLabel)

test = snNetwork()

test.configTF()

test.training(tImage,tLabel)

testPlot(tImage,tLabel,test)

#testRun(testI,testL,test)
