import os
import os.path
import argparse

def startNewPart(fileName, partIndex, sourceLines, trianglesIndexStart):
    
    baseName = os.path.basename(fileName)    
    dir = os.path.dirname(file)

    outputName = "{0}/{1}_{2}.smd".format(dir, baseName, partIndex)

    outputFile = open(path, "wt")

    for i in (0, trianglesIndexStart):
        outputFile.write(sourceLines[i] + "\n")

    return outputFile        


def splitFile(fileName, max_poly):

    fileHandle = open(fileName, "rt")
    lines = fileHandle.readlines()

    trianglesIndexStart = lines.index("triangles")
    partsCount = 0
    polyCount = 0

    linesToWrite = (len(lines) - trianglesIndexStart) / 4

    file = startNewPart(fileName, partsCount, sourceLines, trianglesIndexStart)

    for i in (0, linesToWrite):

        offset = (i * 4) + trianglesIndexStart

        file.write(lines[offset] + "\n")
        file.write(lines[offset + 1] + "\n")
        file.write(lines[offset + 2] + "\n")
        file.write(lines[offset + 3] + "\n")
         
        polyCount += 1

        if (polyCount >= max_poly):
            partsCount += 1
            file.close()
            file = startNewPart(fileName, partsCount, sourceLines, trianglesIndexStart)
    

    file.close()



parser = argparse.ArgumentParser(
                    prog='SMD Splitter',
                    description='Splits big SMD to smaller ones',
                    epilog='Greetings to Xash3D Modding / Disscussion group!')

parser.add_argument('filename')           # positional argument
parser.add_argument('-m', '--max_poly')      # option that takes a value


args = parser.parse_args()

if args.filename.strip() != "":
    SplitFile(args.filename, args.max_poly)    


