import os

def getFileData(filePath):
    data = ""
    if os.path.exists(filePath):
        with open(filePath, "r") as text_file:
            data = text_file.read()
    return data