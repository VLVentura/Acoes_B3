class Parser:
    test = []

    def __init__(self, fileName):
        self.readFile(fileName)

    def readFile(self, fileName):
        with open(fileName, 'r') as file:
            line = file.read()
            self.createCSV(line)
    
    def createCSV(self, line):
        with open('teste.csv', 'a+') as csvFile:
            csvFile.write(line)