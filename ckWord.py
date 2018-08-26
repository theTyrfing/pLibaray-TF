import re
import os
import subprocess
from os import listdir
from shutil import move

def ckTools():
    global msWord
    msWord = ckTool("winword","Microsoft Office")
    global lOffice
    lOffice = ckTool("soffice","LibreOffice 5")

def docTodocx(fs, dirPath):
    if fs.endswith('.doc'):
        filename = os.path.join(dirPath,fs)
        if msWord:
            import win32com.client as win32
            from win32com.client import constants
            save_as_docx(filename)
            nFile = nfile(fs)
            move(nFile, dpath + nFile)
            return nFile
        elif lOffice:
            wpath = nosPath(gWordpath)
            fpath = nosPath(filename)
            dpath = nosPath(dirPath)
            
            subprocess.run([wpath,
                            '--headless',
                            '--convert-to',
                            'docx',
                            fpath])
            nFile = nfile(fs)
            move(nFile, os.path.join(dpath,nFile))
            return nFile
        else:
            return str(fs)
    else:
        return str(fs)
    
def nfile(fs):
    return str(fs).replace(".doc",".docx")

def nosPath(string):
    if string.isspace():
        nString = re.sub(r'(\\)([^\\]+)',
                         lambda x: str('\\'+ '"{}"'.format(str(x.group(2)))),
                         string)
    else:
        nString = string

    return nString

def ckTool(name, dName = ""):
    bFound = False
    
    for d in listdir("C:\\"):
        if os.path.isdir(os.path.join("C:\\",d)):
            if str(d) == "Program Files":
                if bFound != True:
                    bFound = sProgram(name,"C:\\Program Files\\",dName)   
            elif str(d) == "Program Files (x86)":
                if bFound != True:
                    bFound = sProgram(name,"C:\\Program Files (x86)\\",dName)  
            else:
                pass
            
        if bFound == True:
            break

    return bFound

def sProgram(name, path, dNm = ""):
    global gWordpath
    gWordpath = ""

    for d in listdir(path):
        if str(d) == dNm and dNm != "":
            for r,d,f in os.walk(os.path.join(path,d)):
                for files in f:
                    if files == name+".exe":
                        gWordpath = str(os.path.join(r,files))
                        return True
    
    if dNm == "":
        for r,d,f in os.walk(path):
            for files in f:
                if files == name+".exe":
                    gWordpath = str(os.path.join(r,files))
                    return True
    return False

def save_as_docx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)
