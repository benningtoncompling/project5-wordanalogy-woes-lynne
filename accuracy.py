import math

class Accuracy:
    inputFile = ""
    vectorFile = ""
    shouldNormalize = 0
    similarityType = 0
    outFile = ""

    def __init__(self, iF, vF, sN, sT, oF):
        self.inputFile = iF
        self.vectorFile = vF
        self.shouldNormalize = sN
        self.similarityType = sT
        self.outFile = oF

    #First Get the Vector from the Vector File
    def vectorIn(self):
        vectorDict = {}
        vectorRead = [line.split() for line in open(
            self.vectorFile, 'r', encoding='UTF-8').readlines()]
        for item in vectorRead:
            temp = item[1:]
            vectorDict[item[0].lower()] = [float(i) for i in temp]
        return vectorDict

    #Then Get the Input from the Input File
    def inputIn(self):
        inputRead = [line.split() for line in open(
            self.inputFile, 'r', encoding='UTF-8').readlines()]
        for item in inputRead:
            for i in range(len(item)):
                item[i] = item[i].lower()
        return inputRead

    #Useful Methods for Dealing with Data Files
    def normVector(self, vector):
        result = []
        total = 0
        magnitude = 0
        for item in vector:
            total += item ** 2
        magnitude = math.sqrt(total)
        result = [vect/magnitude for vect in vector]
        return result

    def processVector(self, inputRead, vectorDict):
        finalVector = {}
        for item in inputRead:
            try:
                a = item[0]
                b = item[1]
                c = item[2]
                words = a + " " + b + " " + c
                vectorA = vectorDict[a]
                vectorB = vectorDict[b]
                vectorC = vectorDict[c]
            except:
                continue
            total = []
            for i in range(len(vectorA)):
                total.append(vectorB[i]+vectorC[i]-vectorA[i])
            if self.shouldNormalize == 1:
                result = self.normVector(total)
                finalVector[words] = result
            else:
                finalVector[words] = total
        return finalVector
        
    def eucDistance(self, vector1, vector2):
        result = 0
        for i in range(len(vector1)):
            result += (vector1[i] - vector2[i])**2
        ans = math.sqrt(result)
        return ans

    def manhDistance(self, vector1, vector2):
        result = 0
        for item in zip(vector1,vector2):
            result += abs(item[0]-item[1])
        ans = result
        return ans

    def cosDistance(self, vector1, vector2):
        result = 0
        sum1 = 0
        sum2 = 0
        for item in zip(vector1,vector2):
            sum1 += item[0] ** 2
            sum2 += item[1] ** 2
            result += item[0] * item[1]
        ans = result/(math.sqrt(sum1) * math.sqrt(sum2))
        return ans

    def getClosest(self, vector, vectorDict):
        ans = []
        for key, value in vectorDict.items():
            if self.similarityType == 0:
                result = self.eucDistance(vector, value)
                if len(ans) == 0:
                    ans.append(result)
                    ans.append(key)
                elif ans[0] >= result:
                    ans[0] = result
                    ans[1] = key
            elif self.similarityType == 1:
                result = self.manhDistance(vector, value)
                if len(ans) == 0:
                    ans.append(result)
                    ans.append(key)
                elif ans[0] >= result:
                    ans[0] = result
                    ans[1] = key
            elif self.similarityType == 2:
                result = self.cosDistance(vector, value)
                if len(ans) == 0:
                    ans.append(result)
                    ans.append(key)
                elif ans[0] <= result:
                    ans[0] = result
                    ans[1] = key
        return ans

    #Get the final answer
    def finalAns(self, finalVector, inputRead, vectorDict):
        accuracyCount = 0
        resultStrings = []
        count = 0

        for key, value in finalVector.items():
            result = key.split()
            ans = self.getClosest(vector = value,vectorDict = vectorDict)
            result.append(ans[1])
            resultStrings.append(key + " " + ans[1] + "\n")
            if result in inputRead:
                accuracyCount += 1
            count += 1

        finAns = accuracyCount
        with open(self.outFile,"w") as res:
            res.write("".join(resultStrings))
        
        return finAns 
