"""This script's goal is to order a set of disordered files. Specified file types will be moved into directories based on modification/creation date."""
import os
import sys
from unipath import Path
from datetime import datetime

fileExt = ["jpg", "png", "jpeg"] #The script will later look for files with these extensions.

def getPath():
    user_path = input("Enter the directory of the disordered files (\"%PATH%\") or choose the parent directory of the script (\"P(arent)\"): ")
    inputFinished = False
    while not inputFinished:
        if user_path in ["P", "p", "Parent", "parent"]:
            chosenPath = Path.cwd()
            #print(str(chosenPath))
            return chosenPath
            break
        elif user_path not in ["P", "p", "Parent", "parent"]:
            assert os.path.exists(user_path), "Couldn't find the file at: "+str(user_path)
            chosenPath = Path(user_path)
            #print(str(chosenPath))
            return chosenPath
            break
        else:
            print("Unknown error.")
            continue



def orderPy(orderType="m", fileTypes=fileExt):
    """Takes the path from getPath() or call and iterates over all files with specified extensions and stores the timestamps of their last modification."""
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            print(sys.argv[1])
            workPath = Path(sys.argv[1])
        else:
            workPath = getPath()
    #workPath = "C:\\Users\\Johannes\\Desktop\\Test\\"
    fileYM_timestamps = []
    fileY_timestamps = []
    #print(str(workPath))
    directory = os.fsencode(str(workPath))
    print("\nLooking for files:")
    for file in os.listdir(directory):
        filename = os.fsdecode(file) 
        for ext in fileTypes:
            if filename.endswith(ext) or filename.endswith(ext.swapcase()): #or filename.endswith(".xyz") - swapcase for alternate upper and lower case
                if orderType in ["m", "M"]:
                    timestampYM = datetime.fromtimestamp(int(os.path.getmtime(str(Path(workPath, filename))))).strftime("%Y.%m")
                    timestampY = datetime.fromtimestamp(int(os.path.getmtime(str(Path(workPath, filename))))).strftime("%Y")
                    print(filename)
                    fileYM_timestamps.append(timestampYM)
                    fileY_timestamps.append(timestampY)
                elif orderType in ["c", "C"]:
                    timestampYM = datetime.fromtimestamp(int(os.path.getctime(str(Path(workPath, filename))))).strftime("%Y.%m")
                    timestampY = datetime.fromtimestamp(int(os.path.getctime(str(Path(workPath, filename))))).strftime("%Y")
                    print(filename)
                    fileYM_timestamps.append(timestampYM)
                    fileY_timestamps.append(timestampY)
                #getmtime (modification time) - getctime (creation time)
                

    if fileYM_timestamps == [] and fileY_timestamps == []:
        print("\nNo data was found!")
        os.system("pause")
    else:
        pathHandle(fileY_timestamps, fileYM_timestamps, workPath, orderType)
        

def pathHandle(fileY_timestamps, fileYM_timestamps, workPath, orderType):
    """Takes the year and year-month timestamps and uniqifies the lists."""
    #initialize empty work lists for timestamps
    workYM_timestamps = []
    workY_timestamps = []

    #uniqifies year timestamps
    workY_timestamps = uniqify(fileY_timestamps)

    #print year timestamps
    print("\nYear directories found:")
    print(workY_timestamps)

    #uniqifies year-month timestamps
    workYM_timestamps = uniqify(fileYM_timestamps)

    #print year-month timestamps
    print("\nYear-Month sub-directories found:")
    print(workYM_timestamps)

    #iterates over year directories that need to be in dir based on found timestamps
    for year in workY_timestamps:
        yearPath = str(Path(workPath, str(year)))
        #print(yearPath)
        if os.path.exists(yearPath):
            pass
        else:
            Path(yearPath).mkdir()
            if os.path.exists(yearPath):
                print("\nCreated missing directory at: "+yearPath)
            else:
                print("\nAn error occured while creating the directory: "+yearPath)

    #iterates over year-month directories that need to be in dir\year\ based on found timestamps
    for yearMonth in workYM_timestamps:
        year = yearMonth[0:4]
        yearMonthPath = str(Path(workPath, str(year), str(yearMonth)))
        #print(yearMonthPath)
        if os.path.exists(yearMonthPath):
            pass
        else:
            Path(yearMonthPath).mkdir()
            if os.path.exists(yearMonthPath):
                print("\nCreated missing sub-directory at: "+yearMonthPath)
            else:
                print("\nAn error occured while creating the sub-directory: "+yearMonthPath)

    move(workPath, orderType)

def move(workPath, orderType):
    """Takes the current work directory from pathHandle() and iterates over the same files from which the timestamps were extracted and moves them to the newly created directories."""
    print("\nMoving files:")
    hasError = []   #for checking whether there has been an error during the operation
    directory = os.fsencode(str(workPath))
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        for ext in fileExt:
            if filename.endswith("."+ext) or filename.endswith("."+ext.swapcase()):
                if orderType in ["m", "M"]:
                    dirSuffix = datetime.fromtimestamp(int(os.path.getmtime(str(Path(workPath, filename))))).strftime("%Y\%Y.%m")
                elif orderType in ["c", "C"]:
                    dirSuffix = datetime.fromtimestamp(int(os.path.getctime(str(Path(workPath, filename))))).strftime("%Y\%Y.%m")
                movePath = Path(workPath, dirSuffix)
                if not os.path.exists(str(Path(movePath, filename))):
                    os.rename(str(Path(workPath, filename)), str(Path(movePath, filename)))
                    print("\n"+filename+" --> "+movePath)
                    if os.path.exists(str(Path(movePath, filename))):
                        print("\nSuccessfully moved "+filename)
                        hasError.append("0")
                    else:
                        print("\nAn error occured while moving "+filename)
                        hasError.append("1")
                else:
                    print("\nFile "+filename+" already exists.")
                

    finish(hasError)

   
def uniqify(inputList):
    """Uniqifies an inputList and returns outputList"""
    outputList = []
    for item in inputList:
        if not item in outputList:
            outputList.append(item)
    
    return outputList


def finish(errorLog):
    """Takes the error log from move() and finishes the operation by printing whether there has been an error or not."""
    if "1" in errorLog:
        print("\nOperation finished with one or more errors.")
    else:
        print("\nOperation finished successfully.")
    
    os.system("pause")

    #todo: add option to read extensions from text file (normalize entries), think about github publication

orderPy()