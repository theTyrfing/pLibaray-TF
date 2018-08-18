import tensorflow
from openpyxl import load_workbook, Workbook
import win32com.client as win32
from os import listdir
import os
from os.path import isfile, join,isdir
from DialogLib import *

class itemObj:
    pass

    def _init_(self):
        self.iNum  = "00 00 00"
        self.iName = ""
        self.iDecp = "Default"
        self.unit = "Unit"
        self.unitRate = 0.0
        self.contractor = "Test"
        self.date = ""
        self.project = ""
        self.qu = 1

def sfileList(mypath):
    sList =[]
    nList=[]
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for fs in files:
        i = fs.find("-")
        tString = fs[:i-1]
        tString2 = fs[i+1:]
        tString2 = tString2(".docx","")
        tString2 = tString2(".doc","")
        tString = tString.replace(" ","")
        tString = tString[:2]+" "+tString[3:4]+" "+tString[5:6]
        sList = sList.append(tString)
        nList = sList.append(tString2)
    return sList,nList

def bidForm():
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = 0
    word.DisplayAlerts = 0

    tList = []

    fname = pickFile("docx")
    doc = word.Documents.Open(fname)

    bidTable = doc.Tables(1)

    for row in bidTable.Rows:
        for cell in row.Cells:
            if (len(cell.Range.Value)) > 1:
                tList.append(cell.Range.Value)
    return tList

def gatherBids():
    #Item Object Array
    iList = []
    
    #Pick a directory to get information
    pathString = pickDirectory()

    file_names = [os.path.join(pathString, f) 
        for f in os.listdir(pathString) 
        if f.endswith("xlsx")]
        
    for f in file_names:
        print(f)
        if str(f).find(".xlsx") != -1:
            iList.extend(compileItems(str(f)))
    return iList
    
def compileItems(fname):
    wb = load_workbook(fname,data_only=True)
    ws = wb["Detailed"]

    t2List = []    

    nGame = findRows(ws)
    endCol = findCol(ws,nGame[0])

    cList = getContractors(wb,endCol)
    sProj, sDate, sLoc = getInfo(ws)

    print("Compile items")
    
    for i in nGame:
        t2List.extend(getItem(sProj, sDate, sLoc, ws,cList,i,endCol))
        
    return t2List
    
def findRows(ws):
    nGame = []
    
    x = 2
    y = 15
    coBlank = 0
    
    while True:
        if ws.cell(row = y, column = x).value == None:
            coBlank = coBlank + 1
            
        else:
            coBlank = 0
            if ckNum(str(ws.cell(row = y, column = x).value))==True:
                nGame.append(y)

        if coBlank == 20:
            break

        y = y + 1
    return nGame

def findCol(ws,row):
    x = 2
    y = row
    coBlank = 0

    while True:
        if ws.cell(row = y, column = x).value == None:
            coBlank = coBlank + 1
            
        else:
            coBlank = 0

        if coBlank == 5:
            break

        x = x + 1

    x = x - 5
    
    return x

def getContractors(wb,col):
    ws_sum = wb["Summary ALL"]
    contractor = []
    for row in ws_sum.iter_rows(min_row=15, min_col= 2, max_col=col, max_row=15):
        for cell in row:
            if str(cell.value).find("Base BID") != -1:
                pass
            elif str(cell.value).find("Base Bid") != -1:
                pass
            elif str(cell.value).find("BASE BID") != -1:
                pass
            elif str(cell.value).find("AVERAGE BID COST") != -1:
                pass
            elif cell.value == None:
                pass
            else:
                contractor.append(str(cell.value))
    return contractor

def getInfo(ws):
    sProj = ""
    sDate = "" 
    for row in ws.iter_rows(min_row=9, min_col= 2, max_col=6, max_row=12):
        for cell in row:
            iProject = str(cell.value).find("Project :")
            iDate = str(cell.value).find("Date:")
            if iProject != -1:
                sProj = str(cell.value)[(iProject + 9):]
            elif iDate != -1:
                sDate = str(cell.value)[(iDate + 5):]
            else:
                pass
    sLoc = str(ws["B10"].value)
    return sProj, sDate, sLoc

def getItem(sProj, sDate, sLoc, ws,cList,row,col):
    print("Found Item")
    tList = []
    i = 0
    numBool = False
    LS = False
    unitYes = False
    quantity = 1
    unitValue = ""
    for row in ws.iter_rows(min_row=row, min_col= 3, max_col=col, max_row=row):
        for cell in row:
            if str(cell.value).find("N/A") != -1:
                pass
            elif str(cell.value).find("Lump Sum") != -1 or str(cell.value) == "LS":
                unitValue = "LS"
                LS = True
            elif str(cell.value) == "Allowance" or str(cell.value) == "Allow.":
                unitValue = "Allow."
                LS = True
            elif str(cell.value) == "m":
                unitValue = "m"
                unitYes = True
            elif str(cell.value) == "m2" or str(cell.value) == "sq.m":
                unitValue= "sq.m"
                unitYes = True
            elif str(cell.value) == "EA":
                unitValue = "EA"
                unitYes = True
            elif len(str(cell.value)) > 5 and ckNum(str(cell.value)) == False:
                dString = str(cell.value)
            elif ckNum(str(cell.value)) == True:
                if i < len(cList):
                    if LS == False and numBool == True:
                        numBool = False
                        pass
                    elif LS == True and cell.value == 1:
                        pass
                    else:
                        if unitYes == True:
                            quantity = cell.value
                            unitYes = False
                        else:
                            tObj = itemObj()
                            tObj.project = sProj + "-" + sLoc
                            tObj.date = sDate
                            tObj.iDecp = dString
                            tObj.unit = unitValue
                            tObj.qu = quantity
                            tObj.unitRate = cell.value
                            tObj.contractor = cList[i]
                            i = i + 1
                            tList.append(tObj)
                            numBool = True
            else:
                pass

    return tList

def ckNum(value):
    try:
        float(str(value))
        #print("True")
        return True
    except:
        #print("False")
        return False
    
def saveData(iList):
    pathString = pickFile("xlsx")
    wb = load_workbook(pathString)
    ws = wb["Source Data"]
    i = 0 
    while True:
        vl= ws.cell(row = 3+i, column = 1).value
        if vl == None:
            break
        else:
            i = i + 1
    sRow = i + 3
    print(sRow)
    i = 0
    
    for item in iList:
        ws.cell(row = sRow+i, column = 1).value = 1 + ws.cell(row = sRow-1+i, column = 1).value
        ws.cell(row = sRow+i, column = 2).value = item.date
        ws.cell(row = sRow+i, column = 3).value = item.project
        ws.cell(row = sRow+i, column = 5).value = item.iDecp
        ws.cell(row = sRow+i, column = 9).value = item.contractor
        ws.cell(row = sRow+i, column = 11).value = item.unitRate
        ws.cell(row = sRow+i, column = 12).value = item.unit
        ws.cell(row = sRow+i, column = 13).value = item.qu
        i = i + 1
        
    wb.save(pathString)        

saveData(gatherBids())
