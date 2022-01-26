from graphviz import Digraph

class Tube:
    def __init__(self, sample):
        self.original = sample
        self.content = {'volume': 150, self.original: 1}
        self.pipetteVolume = 75

    def add(self, tube):
        """Add (self.pipetteVolume) ul of solution in tube <tube> into this Tube
        """
        if not isinstance(tube, Tube):
            return 'error'
        divider = self.content['volume'] + self.pipetteVolume
        for sample in self.content:
            if sample == 'volume':
                continue
            self.content[sample] = self.content['volume'] * self.content[sample] /divider
        for keyAdd in tube.content:
            if keyAdd == 'volume':
                tube.content['volume'] -= self.pipetteVolume
                continue
            if keyAdd in self.content:
                self.content[keyAdd] += self.pipetteVolume * tube.content[keyAdd] / divider
            else:
                self.content[keyAdd] = self.pipetteVolume * tube.content[keyAdd] / divider
        self.content['volume'] += self.pipetteVolume

    def mix(self, tube):
        """Mix this Tube itself with another tube <tube>
        """
        self.add(tube)
        tube.add(self)

    def getContent(self, delimiter = ' ', *, need_sort = 0):
        """return the string content all content in the tube in form sample: percentage
        """
        if need_sort == 0:
            return delimiter.join([f"{k}: {self.content[k] * 100:.2f}%" for k in self.content if k != 'volume'])
        if need_sort == 200:
            a = [(k, self.content[k] * 100) for k in self.content if k != 'volume']
            a = sorted(a, key = lambda x: x[1])
            return delimiter.join([f"{k}: {v:.2f}%" for k,v in a][::-1])
        if isinstance(need_sort, list):
            a = [(k, self.content[k] * 100) for k in self.content if k in need_sort]
            return delimiter.join([f"{k}: {v:.2f}%" for k,v in a])
        a = [(k, self.content[k] * 100) for k in self.content if k != 'volume']
        a.sort()
        return delimiter.join([f"{k}: {v:.2f}%" for k,v in a])

    def setStatus(self, status):
        """Set the status of this tube ('++' , '+', '-', '+/-')
        """
        self.status = status


class Main:
    def __init__(self):
        self.tubeList = dict()
        self.csvName = "Result.csv"
        self.finalTubeList = []
        self.origin = None
        self.main()

    def main(self):
        self.getCsvName()
        self.csv2TubeList()
        print(f"Start mixing the sample according to the sequence in {self.csvName}")
        print("-" * 100)
        self.getFinalTubeList()
        self.bindStatus(self.finalTubeList)
        print("The result of sample and the contents in all tube are shown below: \n")
        for i in self.finalTubeList:
            print(f'Tube {i.original}\nResult:', i.status,'\nContent:', i.getContent())
        print("-" * 100)
        self.anlalyseAntigen()
        print(f"The origin of hypothetical virus X is predicted to be {' or '.join([i.original for i in self.origin])}")
        print("-" * 100)
        print(f"Simulating how sample in tube {self.origin[0].original} spread within the population")
        print("The spreading sequence is listed as follow: ")
        self.runMap(self.origin[0].original, 'all', needsort = [self.origin[0].original])
        print("-" * 100)
        print("Complete!!!")
        print("If you want to generate map of other sample, you can enter the capital letter code of the sample or you can enter any things to leave.\n")
        runSample = input("> ")
        while runSample in self.tubeList:
            print(f"Start generating map of tube {runSample}")
            mapName = "Tube" + runSample + "Map"
            self.runMap(runSample, 'all', needsort = [runSample], filename = mapName)
            print("-" * 100)
            print("Complete!!!")
            print("If you want to generate map of other samples, you can enter the capital letter code of the sample or you can enter any things to leave.\n")
            runSample = input("> ")
        print("Programme Exit Code 0")


#ask user to input the file name of the csv file that include the ELISA result
    def getCsvName(self):
        """Ask user to input the file name of the csv file of the ELISA result"""
        csvname = input("Name of the .csv file you want to load\n> ")
        #csvname = "result.csv"
        if csvname.find('.csv') == -1:
            csvname += '.csv'
        self.csvName = csvname
        return csvname

#get all the ELISA result from the csv file and put in dict(tubeList) in format {tubeCode: [firstmix, secondmix, thirdmix, <++, +, +/-, ->]}
    def csv2TubeList(self):
        """Get all the ELISA result from the csv file and put in dict(tubeList) in format {tubeCode: [firstmix, secondmix, thirdmix, <++, +, +/-, ->]}
        """
        with open(self.csvName, 'r', encoding = "utf-8") as csv:
            csv.readline()
            for tube in csv:
                tube = tube.strip()
                tubeInfo = tube.split(';')
                self.tubeList[tubeInfo[0]] = tubeInfo[1:]

    def runTube(self, tubeCode, stopCode = None):
        """Get the tube <tubeCode> after the whole mixing process
        """
        if stopCode == None:
            stopCode = tubeCode
        path = self.tubeList[tubeCode][:-1]
        sampleTube = Tube(tubeCode)
        for tube in path:
            if tube == stopCode:
                return sampleTube
            sampleTube.mix(self.runTube(tube, tubeCode))
        return sampleTube

    def getFinalTubeList(self):
        finalTubeList = []
        for tube in self.tubeList:
            finalTubeList.append(self.runTube(tube))
        self.finalTubeList = finalTubeList[:]
        return finalTubeList[:]

    def bindStatus(self, tubeList):
        for tube in self.finalTubeList:
            tube.setStatus(self.tubeList[tube.original][-1])

    def checkAntigen(self, sampleCode):
        """Check if the tube sampleCode is the tube that contain antigen and return similarity correctCase/totalCase
        """
        correctCase = 0
        wrongCase = 0
        for tube in self.finalTubeList:
            if (tube.status == "++" or tube.status == "+") and (sampleCode in tube.content):
                correctCase += 1
                continue
            elif (tube.status == "++" or tube.status == "+") and (sampleCode not in tube.content):
                wrongCase += 1
        similarity = correctCase / (correctCase + wrongCase)
        step = 0.5/len(self.finalTubeList)
        if similarity < (1 - step):
            return correctCase / (correctCase + wrongCase)
        for tube in self.finalTubeList:
            if (tube.status == "-") and (sampleCode in tube.content):
                similarity -= step
        return similarity


    def anlalyseAntigen(self):
        """Analyze which tube got the higher probability to be original antigen tube
        """
        maxSimilarity = 0
        nowAntigen = []
        for tube in self.finalTubeList:
            similarity = self.checkAntigen(tube.original)
            print(f"{similarity * 100:6.2f}% of the positive result samples contain sample in Tube {tube.original}")
            if similarity > maxSimilarity:
                nowAntigen = [tube]
                maxSimilarity = similarity
            elif similarity == maxSimilarity:
                nowAntigen.append(tube)
        print("-" * 100)
        if len(nowAntigen) <= 1:
            self.origin = nowAntigen
            return nowAntigen
        mostList = []
        for tube in self.finalTubeList:
            if tube.status == "++":
                maximum = max([tube.content[i.original] for i in nowAntigen])
                maxList = [x for x in nowAntigen if tube.content[x.original] == maximum]
                mostList.extend(maxList)
                print(f"Tube {' or '.join([x.original for x in maxList])} have highest portion in tube {tube.original} labelled with '++'")
        tubeTimespp = []
        for tube in nowAntigen:
            tubeTimespp = [(x, maxList.count(x)) for x in nowAntigen]
        maxTimes = max([x[1] for x in tubeTimespp])
        nowAntigen = [x[0] for x in tubeTimespp if x[1] == maxTimes]
        self.origin = nowAntigen
        return nowAntigen

    def runRoute(self, tubeCode, startCode = None):
        """Get the tube <tubeCode> route map to infect [((tube1, tube1.content),(tube2, tube2.content))]
        """
        route = []
        path = self.tubeList[tubeCode][:-1]
        sampleTube = Tube(tubeCode)
        is_Trigger = False
        for toTubeCode in path:
            if startCode == None:
                route.append((('start', sampleTube.getContent('\n', need_sort = 1)),(tubeCode, sampleTube.getContent('\n', need_sort = 1))))
                startCode = tubeCode
                is_Trigger = True
            if is_Trigger:
                toTube = self.runTube(toTubeCode, sampleTube.original)                            #get the object of the tube when (before) pass to that tube
                print(tubeCode +" to "+ toTubeCode)
                #print(f"self.runTube({toTubeCode}, {sampleTube.original})\n"+toTube.getContent("\n", need_sort = 1))
                sampleTube = self.runTube(tubeCode, toTubeCode)
                backupsample = (tubeCode, sampleTube.getContent('\n', need_sort = 1))
                route.append((backupsample, (toTubeCode, toTube.getContent("\n", need_sort = 1))))
                sampleTube.mix(toTube)
                route.extend(self.runRoute(toTube.original, tubeCode))
                #print(toTube.original, tubeCode, path)
                #sampleTube continue pass
                continue
            if toTubeCode == startCode:
                is_Trigger = True
        return route[:]

    def runMap(self, tubeCode, need_content = False, needsort = 0, filename = "route_map"):
        rmap = Digraph("route", filename = filename)
        route = self.runRoute(tubeCode)
        vertices = dict()
        for i in route:
            front = i[0][0]
            frontContent = i[0][1]
            after = i[1][0]
            afterContent = i[1][1]
            if front == 'start':
                continue
            if front not in vertices:
                vertices[front] = 1
                rmap.node(front + str(vertices[front]), label = self.cell(front, frontContent, need_content, needsort = needsort))
            vertices[after] = 1 if after not in vertices else vertices[after] + 1
            rmap.node(after + str(vertices[after]), label = self.cell(after, afterContent, need_content, needsort = needsort))
            rmap.edge(front + str(vertices[front]), after + str(vertices[after]))
        rmap.view()

    def cell(self, tubeCode, contentString = '', need_content = False, needsort = 0):
        if not need_content:
            return tubeCode
        if need_content == 'all':
            return tubeCode + '\n' + self.runTube(tubeCode).getContent('\n', need_sort = needsort)
        if need_content == 1:
            return tubeCode + '\n' + contentString


a = Main()
