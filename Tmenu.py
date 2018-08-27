from ckWord import ckTools
from dataProg import compile_iObj, compile_sObj, compile_gObj, ckNum, savMSingle, callDialogs
from dataProg import sMaker,uMaker,mdMaker,uiChoice, savModUnit, savgObj,compile_Cat
from tClasses import gObj
from mlProg import mlSave

iList = []
sList = []
gList = []
cList = []
boolp = False
skipTen = 10
    
keyChain =['A','B','C','D','E']

labChain = ["Get Section List from Spec Directory",
                "Get Unit Price Bid Data from Bid Data",
                "Get Bid Data for Machine Learning",
                "Process Bid Data for Machine Learning",
                "Unit Pricing Data Processing"]

funChain = ["sMaker","uMaker","mdMaker","mlSave","uiChoice"]

unitChain = ["Spec #","Name","Description","Unit","Unit Rate","Contractor",
             "Date","Project","Quantity","Service Life","Company Code","Notes",
             "Uniformat","GroupID"]

unFun = []
for x in range(0,len(unitChain)):
    if x == 0:
        unFun.append("mSpecS")
    elif x == 13:
        unFun.append("groupMenu")
    elif x ==14:
        unFun.append("savEntry")
    else:
        unFun.append("modObj")

iObjName = ['iNum','iName', 'iDecp', 'unit', 'unitRate','contractor','date'
            ,'project', 'qu', 'sLife', 'cCode', 'notes','uni',['gID', 'sID']]

gChain = ["Spec #","Name","Description","Unit","UniFormat",
          "Company Code","GroupID", "Notes"]

sdivisions = [0,1,2,3,4,5,6,7,8,9,15,23,26,32]

specChain = []
for x in sdivisions:
    specChain.append("Division " + str(x))


def dicFunc(name, arg = None):
    dicGlob = {"sMaker":sMaker,
               "uMaker":uMaker,
               "mdMaker":mdMaker,
               #"mlSave":mlSave,
               "uiChoice":itemProgMenu,
               "mSpecS": mSpecS,
               "groupMenu": groupMenu,
               "modObj": modObj,
               "savEntry":savEntry,
               "create_gObj":create_gObj}
    
    if arg == None:
        return dicGlob[name]()
    else:
        return dicGlob[name](arg)

#Menu Item Class
class menuItem:
    pass

    def _init_(self):
        self.key = "A"
        self.mName= "Default"
        self.func = ""
        self.reExp = False
        self.fArg = []
        self.fVar = 0

    def iStarter(self):
        self.key = "A"
        self.mName= "Default"
        self.func = ""
        self.reExp = False
        self.fArg = []
        self.fVar = 0

    def rFunc(self):
        dicFunc(self.func,self.fArg)

    def vFunc(self):
        return dicFunc(self.func,self.fArg)

#Menu Class
class cMenu:
    pass

    def _init_(self):
        self.mID = []
        self.mItem = []
        self.mCName = "Menu"
        self.mCKey = ""

    def mStarter(self):
        self.mID = []
        self.mItem = []
        self.mCName = "Menu"
        self.mCKey = ""

    def addMItem(self, aName, aKey, aFunc = "", aArg = None, aRet = False ,aVar = None):
        tObj = menuItem()
        tObj.iStarter()
        tObj.key = aKey
        tObj.mName = aName
        tObj.func = aFunc
        tObj.reExp = aRet
        if aArg != None:
            tObj.fArg.append(aArg)
        else:
            tObj.fArg = None
        if aVar != None:
            tObj.fVar = aVar

        nID = len(self.mID) + 1
        
        self.mItem.append(tObj)
        self.mID.append(nID)
        
    def addMenu(self,mMenu,aName = None, aKey = None):
        nID = len(self.mID) + 1
        tObj = mMenu
        self.mID.append(nID)
        if aName != None:
            tObj.mCName = aName
        if aKey != None:
            tObj.mCKey = aKey
        self.mItem.append(tObj)
        
    def dsMenu(self):
        mTemp = "[...] - ***"
        nRange = len(self.mID)
        
        print("-------" + self.mCName + "-------")
        
        for i in range(0,nRange):
            try:
                aKey = self.mItem[i].key
                aName = self.mItem[i].mName
                print((mTemp.replace('...',str(aKey))).replace('***',str(aName)))
            except:
                aKey = self.mItem[i].mCKey
                aName = self.mItem[i].mCName
                print((mTemp.replace('...',str(aKey))).replace('***',str(aName)))
        print((mTemp.replace('...',"/b")).replace('***',"Done or Quit"))
        print("-------" + self.mCName + "-------")

    def MLoop(self):
        while True:
            if self.inputMenu() or boolp == True:
                break

    def Vloop(self):
        while True:
            value = self.rValMenu()
            if value != None:
                return value
            
    def rValMenu(self):
        self.dsMenu()
        iKey = input(">>>")
        iKey = str(iKey)
        
        for v in self.mItem:
            
            
            if iKey == "/b":
                return "/b"
                
            try:
                if v.key == iKey:
                    
                    if v.func == "":
                        return v.fVar
                    else:
                        return v.vFunc()
                    
            except:
                if v.mCKey == iKey:
                    value2 = v.Vloop()
                    if value2 != "/b" and value2 != None:
                        return value2
                
        return None
        
    def inputMenu(self):
        self.dsMenu()
        iKey = input(">>>")
        iKey = str(iKey)
        
        for m in self.mItem:
            if iKey == "/b":
                return True
            elif iKey == "skip":
                global skipTen
                skipTen = 0
                return True
            else:
                pass
            
            try:
                if m.key == iKey:
                    if m.func != "":
                        m.rFunc()
                        break
            except:
                if m.mCKey == iKey:
                    m.MLoop()
                    break
        return False

def modObj(argList):
    getPrintout(argList)
    iPut = input('Input revised (To Cancel type \\cancel): ')
    if iPut != "\\cancel":
        setattr(argList[0][argList[1]],argList[2],iPut)

def getPrintout(argList):
    print("S#: " + str(argList[0][argList[1]].iNum))
    print("Name: " + str(argList[0][argList[1]].iName))
    print("Description: " + "\n" + str(argList[0][argList[1]].iDecp).replace("\n",""))
    print("Project: " + str(argList[0][argList[1]].project)+"\n")
    print("Current Value" +  ": \n" + str(getattr(argList[0][argList[1]],argList[2]))+"\n")
    
def getPrintoutlite(argList):
    print("S#: " + str(argList[0][argList[1]].iNum))
    print("Name: " + str(argList[0][argList[1]].iName))
    print("Description: \n" + str(argList[0][argList[1]].iDecp).replace("\n",""))
    print("\nProject: " + str(argList[0][argList[1]].project))
    print("\nContact: " + str(argList[0][argList[1]].contractor))
    print("\nUnit Price: " + str(argList[0][argList[1]].unitRate))
    print("\nUnit: " + str(argList[0][argList[1]].unit))
    print("\nUniformat: " + str(argList[0][argList[1]].uni))
    print("\nGroup ID: " + str(argList[0][argList[1]].gID))
    print("\nSub-Group ID: " + str(argList[0][argList[1]].sID))

def autoKey(tList):
    nList = []
    for c in range (0,len(tList)):
        nList.append(str(c))

    return nList

def mSpecS(argList):
    getPrintoutlite(argList)
    lSpec = autoKey(specChain)
    menuSpec = cMenu()
    menuSpec.mStarter()
    global sList

    for k in range(0,len(specChain)):
        tMenuObj = cMenu()
        tMenuObj.mStarter()
        miniKey = 0
        for sg in sList:
            if sg.division != "A":
                if int(sg.division) == int(sdivisions[k]):
                    if sg.sNum != "":
                        tMenuObj.addMItem(sg.sNum + "-" + sg.sName,str(miniKey),"",None,False,sg.sID)
                        miniKey = miniKey + 1

        menuSpec.addMenu(tMenuObj,specChain[k],lSpec[k])

    menuSpec.addMItem("None","X","",None,False,"None")

    index = menuSpec.Vloop()
    
    if index != "/b" and index != "None":
        assignValue(argList[0],argList[1],argList[2],sList[index-1].sNum)
    elif index == "None":
        assignValue(argList[0],argList[1],argList[2],"None")
    else:
        pass
    
def mSpecL(argList):
    lSpec = autoKey(specChain)
    menuSpec = cMenu()
    menuSpec.mStarter()
    global sList

    for k in range(0,len(specChain)):
        tMenuObj = cMenu()
        tMenuObj.mStarter()
        miniKey = 0
        for sg in sList:
            if sg.division != "A":
                if int(sg.division) == int(sdivisions[k]):
                    if sg.sNum != "":
                        tMenuObj.addMItem(sg.sNum + "-" + sg.sName,str(miniKey),"",None,False,sg.sID)
                        miniKey = miniKey + 1

        
        menuSpec.addMenu(tMenuObj,specChain[k],lSpec[k])
        
    menuSpec.addMItem("None","X","",None,False,"None")
    
    index = menuSpec.Vloop()
    if index != "/b" and index != "None":
        return sList[index-1].sNum
    elif index == "None":
        return "None"
    else:
        return "/b"

def groupMenu(argList):
    getPrintoutlite(argList)
    menuG = cMenu()
    menuG.mStarter()
    global gList
    global cList

    menuG.addMItem("New Generic Item","/N","create_gObj",argList)

    for con in range(0,len(cList)):
        tMenuObj = cMenu()
        tMenuObj.mStarter()
        
        miniKey = 0
        tMenuObj.addMItem("New Generic Item","/N","create_gObj",argList)
        for k in range(0,len(gList)):
            if gList[k].gID == cList[con].cID:
                tMenuObj.addMItem(gList[k].iName,str(miniKey),"",None,False,k)
                miniKey = miniKey + 1

        menuG.addMenu(tMenuObj,cList[con].cName,cList[con].cID)

    index = menuG.Vloop()

    if index != "/b" and index != "<n>":
        assignValue(argList[0],argList[1],argList[2][0],gList[index].gID)
        assignValue(argList[0],argList[1],argList[2][1],gList[index].sID)

def assignValue(tObj,index,varName,value):
    setattr(tObj[index],varName,value)

def itemProgMenu():
    iSetting = ""
    fSetting = ""
    ssSetting = ""
    
    print("Starting Data Processing Routine...")
    while iSetting != "P" and iSetting != "B":
        iSetting = input("Saving Setting => Progressive Save [P] or Batch [B]: ")
        if iSetting != "P" and iSetting != "B":
            print("Invalid Entry.")

    while fSetting != "A" and fSetting != "S" and fSetting != "G":
        fSetting = input("Filter Setting => All [A], Spec Section [S], & Grouping[G]: ")
        if fSetting != "A" and fSetting != "S" and fSetting != "G":
            print("Invalid Entry.")

    while ssSetting != "Y" and ssSetting != "N":
        ssSetting = input("Duplicate Entry Setting => Do you want skip & write over duplicate entries (Y/N): ")
        if ssSetting != "Y" and ssSetting != "N":
            print("Invalid Entry.")
    
    iMenu = cMenu()
    iMenu.mStarter()
    uKey = autoKey(unitChain)
    
    global iList 
    global gList 
    global sList
    global cList
    global boolp
    global skipTen

    callDialogs()
    
    iList = compile_iObj()
    gList = compile_gObj()
    sList = compile_sObj()
    cList = compile_Cat()

    for i in range(0,len(unitChain)):
        iMenu.addMItem(unitChain[i],uKey[i],unFun[i])
        
    for iC in range(0,len(iList)):
        boolp = False
        tSpec = iList[iC].iNum
        tGID = iList[iC].gID
        bolEntry = sameEntry(iC,iList,ssSetting)
        
        if skipTen >= 10 and ckEnt(fSetting,tSpec,tGID) == True and bolEntry == True:
            for i in range(0,len(unitChain)):
                if i != 14:
                    iMenu.mItem[i].fArg = [iList,iC,iObjName[i]]
                else:
                    pass                

            print("ID#:"+str(iC+1))
            getPrintoutlite([iList,iC,iObjName[0]])
            
            iMenu.MLoop()
            if iSetting == "P" and skipTen >=10:
                savMSingle(iC,iList)
        elif skipTen >= 10 and ckEnt(fSetting,tSpec,tGID) == True and bolEntry == False:
            print("Duplicate Entry - Overwriting certain values...")
            sameOverwrite(bolEntry,iC,iList)
            if iSetting == "P" and skipTen >=10:
                savMSingle(iC,iList)
        elif skipTen >= 10 and ckEnt(fSetting,tSpec,tGID) == False:
            pass
        else:
            skipTen = skipTen + 1
        iC = iC + 1

    if iSetting == "B":
        savModUnit(iList)

    boolp = False

def ckEnt(fSet,sNum,gid):
    if fSet == "A":
        return True
    elif fSet == "S":
        if sNum == "" or sNum == None:
            return True
        else:
            return False
    elif fSet == "G":
        if gid == "" or gid == None:
            return True
        else:
            return False
    else:
        return False

def savEntry():
    global boolp
    boolp = True

def sameEntry(index, itemList, ss):
    if ss == "Y":
        if itemList[index].iDecp == itemList[index-1].iDecp:
            return False
        else:
            return True
    else:
        return True
    
def sameOverwrite(bol, index, itemList):
    if bol == False:
        itemList[index].iName = itemList[index-1].iName
        itemList[index].iNum = itemList[index-1].iNum
        itemList[index].sLife = itemList[index-1].sLife
        itemList[index].cCode = itemList[index-1].cCode
        itemList[index].notes = itemList[index-1].notes        
        itemList[index].gID = itemList[index-1].gID
        itemList[index].sID = itemList[index-1].sID
        itemList[index].uni = itemList[index-1].uni
    
def create_gObj(argList):
    global gList

    print("Adding new generic item:")
    
    tObj=gObj()
    print("Select Spec. Section")
    tObj.iNum  = mSpecL(argList)               #Section Number
    tObj.iName = input("New Name:")            #Name of Item
    tObj.iDecp = input("New Description:")     #Description
    tObj.unit = input("New Unit:")             #Unit
    tObj.uniForm = input("New Uniformat Code:")#Contractor 
    tObj.sLife = input("New Service Life:")    #Service Life
    tObj.cCode = input("New Company Code:")    #Company Code
    tObj.notes = input("Notes:")               #Notes
    tObj.gID = input("Assign Group ID:")       #Group ID
    tSID = 1
    for gItem in gList:
        if gItem.gID == tObj.gID:
            tSID = tSID + 1
    tObj.sID = tSID                            #SubGroup ID

    if input("Confirm save (Y/N):") == "Y":
        gList.append(tObj)
        savgObj(tObj)
        return "<n>"
    else:
        return "/b"
                   
def startup():
    
    ckTools()
    print("Welcome to Data Processing Module")

    mainMenu = cMenu()
    mainMenu.mStarter()
    
    for k in range(0,len(keyChain)):
        mainMenu.addMItem(labChain[k],keyChain[k],funChain[k])

    mainMenu.MLoop()


