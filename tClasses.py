class itemObj:
    pass

    def _init_(self):
        self.iNum  = "00 00 00"   #Section Number
        self.iName = ""           #Name of Item
        self.iDecp = "Default"    #Description
        self.unit = "Unit"        #Unit 
        self.unitRate = 0.0       #Unit Rate
        self.contractor = "Test"  #Contractor 
        self.date = ""            #Date
        self.project = ""         #Project Name
        self.qu = 1               #Quantity
        self.nID = 0              #Internal ID for duplicates
        self.sLife = 0            #Service Life
        self.cCode =""            #Company Code
        self.notes = ""           #Notes
        self.gID = ""             #Group ID
        self.sID = 0              #SubGroup ID
        self.uni = ""             #Uniformat

#Section Class
class sObj:
    pass

    def _init_(self):
        self.sID = 0              #ID
        self.sNum  = "00 00 00"   #Section Number
        self.sName = "Default"    #Section Name
        self.sPage = 1            #Pages
        self.state = 0            #State
        self.related = []         #Related
        self.division = ""        #Section Division

#Generic Item Class Object
class gObj:
    pass

    def _init_(self):
        self.iNum  = "00 00 00"                 #Section Number
        self.iName = ""                         #Name of Item
        self.iDecp = "Default"                  #Description
        self.unit = "Unit"                      #Unit 
        self.unitRate = "=AVGCOND(A5,B5)"       #Service Unit Rate
        self.uniForm = "Test"                   #UniForm 
        self.cCode = ""                         #Company Code
        self.sLife = ""                         #Avg Service Life
        self.gID = ""                           #Group ID
        self.sID = 0                            #SubGroup ID
        self.notes = ""                         #Notes

#Data Class
class dObj:
    pass

    def _init_(self):
        self.sData = ""
        self.sNum = "00 00 00"

#Categories Object
class cObj:
    pass

    def _init_(self):
        self.cID = ""
        self.cName = ""


