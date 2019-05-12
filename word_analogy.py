import accuracy
import os
import sys

vectorFile = sys.argv[1]
openDir = sys.argv[2]
outDir = sys.argv[3]
evalFile = sys.argv[4]
shouldNormalize = int(sys.argv[5])
similarityType = int(sys.argv[6])

fileList = os.listdir(openDir)
eval = []
count = 0
totalLen = len(fileList)

for item in fileList:
    count += 1
    inFiles = os.path.join(openDir, item)
    outName = "output" + str(shouldNormalize) + str(similarityType) + "-" + str(item)
    outFiles = os.path.join(outDir, outName)
    
    ac1 = accuracy.Accuracy(iF = inFiles, 
                            vF = vectorFile, 
                            sN = shouldNormalize, 
                            sT = similarityType, 
                            oF = outFiles)
    vectorDict = ac1.vectorIn()
    inputRead = ac1.inputIn()
    finalVector = ac1.processVector(vectorDict=vectorDict, inputRead=inputRead)
    ans = ac1.finalAns(vectorDict=vectorDict,
                       inputRead=inputRead, 
                       finalVector=finalVector)
    fileName = str(item).split(".")[0]
    eval.append(fileName + ": " + str(ans/len(inputRead)) + "\n")
    print(fileName + " " + str(count) + "/" + str(totalLen))

finalEval = "".join(eval)
with open(evalFile,"w") as eva:
    eva.write(finalEval)
