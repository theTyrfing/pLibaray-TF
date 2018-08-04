#import sys
#sys.path.append('C:\Users\Regan\Documents\GitHub\pLibaray-TF')

from TFuLibaray import *

dirString = pickDirectory()

print (dirString)

tImage, tLabel = loadPic(dirString)

#dImages(tImage, tLabel)

test = snNetwork()

print (test.seed)

test.configTF()

testPrint(test)

test.training(tImage,tLabel)

testPlot(tImage,tLabel,test)
