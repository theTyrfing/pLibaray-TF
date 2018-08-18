from tkinter import Tk, filedialog

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
    fname = filedialog.askopenfilename(initialdir = "/",\
                                       title = "Select file",\
                                       filetypes = ((fExt+" files","*."+fExt),\
                                                    ("all files","*.*")))
    fLocation.destroy()
    if fname == "":
        return ""
    else:
        return fname

def saveFile(fExt):
    fLocation = Tk()
    fname = filedialog.asksaveasfilename(initialdir = "/",\
                                         title = "Select file",\
                                         filetypes = ((fExt+" files","*."+fExt),
                                                      ("all files","*.*")))
    fLocation.destroy()
    if fname == "":
        return ""
    else:
        return fname
