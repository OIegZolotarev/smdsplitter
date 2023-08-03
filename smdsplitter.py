import os
import os.path
import argparse

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



parser = argparse.ArgumentParser(
                    prog='SMD Splitter',
                    description='Splits big SMD to smaller ones',
                    epilog='Greetings to Xash3D Modding / Disscussion group!')

parser.add_argument('filename')           # positional argument
parser.add_argument('-m', '--max_poly', type=int)      # option that takes a value


args = parser.parse_args()

if args.filename.strip() != "":
    splitFile(args.filename, args.max_poly)    


