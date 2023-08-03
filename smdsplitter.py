import os
import os.path
import argparse
import keyboard

def startNewPart(fileName, partIndex, sourceLines, trianglesIndexStart):
    
    baseName = os.path.basename(fileName)[:-4]
    absPath = os.path.abspath(fileName)
    dir = os.path.dirname(absPath)

    outputName = "{0}/{1}_{2}.smd".format(dir, baseName, partIndex)

    outputFile = open(outputName, "wt")

    for i in range(0, trianglesIndexStart):
        outputFile.write(sourceLines[i])

    return outputFile        


def splitFile(fileName, max_poly):

    silentMode = True

    if max_poly == None:   
        while True:
            try:
                max_poly = int(input("Enter polygons limit per bodypart:"))
                silentMode = False
                break
            except:
                continue

    fileHandle = open(fileName, "rt")
    lines = fileHandle.readlines()

    trianglesIndexStart = lines.index("triangles\n") + 1
    partsCount = 0
    polyCount = 0

    polyToWrite = (int)(((len(lines) - 1) - (trianglesIndexStart)) / 4)

    file = startNewPart(fileName, partsCount, lines, trianglesIndexStart)

    for i in range(0, polyToWrite):

        offset = (i * 4) + trianglesIndexStart

        file.write(lines[offset])
        file.write(lines[offset + 1])
        file.write(lines[offset + 2])
        file.write(lines[offset + 3])
         
        polyCount += 1

        if (polyCount >= max_poly):
            partsCount += 1
            file.write("end\n")
            file.close()            
            file = startNewPart(fileName, partsCount, lines, trianglesIndexStart)
            polyCount = 0
    

    file.write("end\n")
    file.close()

    if silentMode == False:

        baseName = os.path.basename(fileName)[:-4]
        
        for i in range(0, partsCount + 1):
            print("$body \"{0}_{1}\" \"{0}_{1}\"".format(baseName, i))

        saveTemplate = input("Save QC template? (y/n)");
    
        if saveTemplate.lower() == "y":
            absPath = os.path.dirname(os.path.abspath(fileName));
            
            fileName = input("File name ({0}.qc):".format(baseName))

            if  fileName.strip() == "":
                fileName = "{0}.qc".format(baseName)
    
            outputFile = open(absPath + "/" + fileName, "wt")
            
            for i in range(0, partsCount + 1):
                outputFile.write("$body \"{0}_{1}\" \"{0}_{1}\"\n".format(baseName, i))

            outputFile.close()

    


    else:
        baseName = os.path.basename(fileName)[:-4]

        for i in range(0, partsCount + 1):
            print("$body \"{0}_{1}\" \"{0}_{1}\"".format(baseName, i))

parser = argparse.ArgumentParser(
                    prog='SMD Splitter',
                    description='Splits big SMD to smaller ones',
                    epilog='Greetings to Xash3D Modding / Disscussion group!')

parser.add_argument('filename')           # positional argument
parser.add_argument('-m', '--max_poly', type=int)      # option that takes a value


args = parser.parse_args()

if args.filename.strip() != "":
    splitFile(args.filename, args.max_poly)    


