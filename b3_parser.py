from itertools import islice

class CreateCSV:

    def __init__(self, fileName):
        self.readFile(fileName)

    def readFile(self, fileName):
        header = ('TIPREG,DATA,CODBDI,CODNEG,TPMERC,NOMRES,ESPECI,PRAZOT,MODREF,PREABE,PREMAX,' +
                  'PREMIN,PREMED,PREULT,PREOFC,PREOFV,TOTNEG,QUATOT,VOLTOT,PREEXE\n'
        )

        with open(fileName, 'r') as file:
            self.writeCSV(header)
            for line in islice(file, 1, None):
                line = self.parser(line)
                self.writeCSV(line)
    
    def writeCSV(self, line):
        with open('COTAHIST_A2019.csv', 'a+') as csvFile:
            csvFile.write(line)

    def parser(self, line):
        TIPREG = line[0:2]
        DATA = line[2:10]
        CODBDI = line[10:12]
        CODNEG = line[12:24].strip()
        TPMERC = line[24:27]
        NOMRES = line[27:39].strip()
        ESPECI = line[39:49].strip()
        PRAZOT = line[49:52].strip()
        MODREF = line[52:56].strip()
        PREABE = line[56:69]
        PREMAX = line[69:82]
        PREMIN = line[82:95]
        PREMED = line[95:108]
        PREULT = line[108:121]
        PREOFC = line[121:134]
        PREOFV = line[134:147]
        TOTNEG = line[147:152]
        QUATOT = line[152:170]
        VOLTOT = line[170:188]
        PREEXE = line[188:201]

        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n" \
               .format(
                   TIPREG, DATA, CODBDI, CODNEG, TPMERC, NOMRES, ESPECI, PRAZOT, MODREF, PREABE,
                   PREMAX, PREMIN, PREMED, PREULT, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT, PREEXE
                )
        