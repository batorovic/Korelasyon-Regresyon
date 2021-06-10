import math
import pandas as pd
import random


class ExcelTo:
    def __init__(self):
        self.dataFrame = 0
        self.liste = []

    def readDataFromExcel(self):
        self.dataFrame = pd.read_excel(r"veriSeti.xlsx", keep_default_na=False)

        # Excel dosyasini scriptin oldugu yerden direkt okumaktadir.
        # return self.dataFrame

        # excelden columnlari okuyunca bos olan columnlar unnamed olarak geliyor onlari silme islemi.
        # print(self.dataFrame.columns)
        self.dataFrame = self.dataFrame.loc[:, ~self.dataFrame.columns.str.contains('^Unnamed')]

    def convertToList(self, data):
        self.liste = []

        for item in data:
            if item == "":
                break
            else:
                self.liste.append(item)
        return self.liste


class Formulas():
    def __init__(self, reklam, telefon, satislar, reklamTest, telefonTest, satislarTest):
        self.n = len(satislar)  # hepsinin uzunlugu aynı olacagi icin 1 tanesinin lenini almak yeterli.
        self.rData = 0
        self.reklam = reklam
        self.telefon = telefon
        self.satislar = satislar
        self.datas = {}

        self.reklamTest = reklamTest
        self.telefonTest = telefonTest
        self.satislarTest = satislarTest

        self.deneme = {}

    def getAvg(self, data):
        sum = 0
        for item in data:
            sum += item
        return sum / self.n

    def sum(self, data):
        sum = 0
        for item in data:
            sum += item
        return sum

    def sumOfXY(self, x, y):
        sum = 0
        for index in range(self.n):
            sum += x[index] * y[index]
        return sum

    def sumOfSquare(self, data):
        sum = 0
        for item in data:
            sum += item ** 2
        return sum

    def avgSquare(self, data):
        return self.getAvg(data) ** 2

    def setDatas(self):
        self.datas = {
            "X1": {
                'x1': 'Reklam',
                # 'X_EGITIM_VERILERI': self.reklam,
                'xValues': self.reklam,
                # 'X_TEST_VERILERI': [],
                'X_TEST_VERILERI': self.reklamTest,
                'y^(Egitim Tahmini Degerler)': [],
                'y^(Test Tahmini Degerler)': [],
                'avgX': self.getAvg(self.reklam),
                'sumOfX': self.sum(self.reklam),
                'sumOfXY': self.sumOfXY(self.reklam, self.satislar),
                'sumSquareOfX': self.sumOfSquare(self.reklam),
                'avgSquareOfX': self.avgSquare(self.reklam),
                'SSE_EGITIM': 0,
                'SSE_TEST': 0
            },
            'X2': {
                'x2': 'Telefon',
                # 'X_EGITIM_VERILERI': self.telefon,
                'xValues': self.telefon,
                # 'X_TEST_VERILERI': [],
                'X_TEST_VERILERI': self.telefonTest,
                'y^(Egitim Tahmini Degerler)': [],
                'y^(Test Tahmini Degerler)': [],
                'avgX': self.getAvg(self.telefon),
                'sumOfX': self.sum(self.telefon),
                'sumOfXY': self.sumOfXY(self.telefon, self.satislar),
                'sumSquareOfX': self.sumOfSquare(self.telefon),
                'avgSquareOfX': self.avgSquare(self.telefon),
                'SSE_EGITIM': 0,
                'SSE_TEST': 0
            },
            'Y': {
                'Y': 'Satislar',
                'Y_VALUES': self.satislar,
                'Y_TEST_VERILERI': self.satislarTest,
                'y^(Egitim Tahmini Degerler)': [],
                'y^(Test Tahmini Degerler)': [],
                'avgY': self.getAvg(self.satislar),
                'sumOfY': self.sum(self.satislar),
                'sumSquareOfY': self.sumOfSquare(self.satislar),
                'avgSquareOfY': self.avgSquare(self.satislar),
            },
        }

    def getDatas(self):
        return self.datas


class Korelasyon():  # Formulas:
    def __init__(self, formulas, n):
        self.n = n
        self.datas = formulas.getDatas()
        self.formuller = formulas

    def setKorelasyon(self):
        self.datas['X1']['r1'] = float("%0.5f" % (self.korelasyonCalculator("X1")))
        self.datas['X2']['r2'] = float("%0.5f" % (self.korelasyonCalculator("X2")))

        self.korelasyonDecider()

    def korelasyonCalculator(self, data):
        return (self.datas[data]['sumOfXY'] - self.n * self.datas[data]['avgX']*self.datas['Y']['avgY']) / math.sqrt((self.datas[data]['sumSquareOfX'] - self.n*self.datas[data]['avgSquareOfX']) * ((self.datas['Y']['sumSquareOfY'] - self.n*self.datas['Y']['avgSquareOfY'])))

    # fazladan olabilir  silinebilir bu !
    def korelasyonDecider(self):
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.rData = self.datas['X1']['r1']
        else:
            self.rData = self.datas['X2']['r2']


class Korelasyon2():
    def __init__(self, formulas, columnCount):
        self.n = len(formulas.deneme['X1']['X_EGITIM_VALUES'])  # fark etmez herhangi birinin egitim uzunlugu olabilir
        self.datas = formulas.deneme
        self.columnCount = columnCount

    def setKorelasyon(self):
        for index in range(1, self.columnCount - 1):
            key = ('X' + str(index))
            r = ('r') + str(index)
            self.datas[key][r] = float("%0.5f" % (self.korelasyonCalculator(key)))

        # self.datas['X1']['r1'] = float("%0.5f" % (self.korelasyonCalculator("X1")))
        # self.datas['X2']['r2'] = float("%0.5f" % (self.korelasyonCalculator("X2")))

    def korelasyonCalculator(self, key):
        return (self.datas[key]['sumOfXY'] - self.n * self.datas[key]['avgX']*self.datas['Y']['avgY']) / math.sqrt((self.datas[key]['sumSquareOfX'] - self.n*self.datas[key]['avgSquareOfX']) * ((self.datas['Y']['sumSquareOfY'] - self.n*self.datas['Y']['avgSquareOfY'])))


class Regresyon():  # Formulas#):
    # def __init__(self, formulas, n, reklam, telefon, satislar):
    #     super(Regresyon, self).__init__(reklam, telefon, satislar)
    def __init__(self, formulas, n, egitimIndexes, orginalDataLength):

        self.formula = formulas
        self.n = n
        self.selectedData = {}
        self.datas = formulas.getDatas()
        self.egitimIndexes = egitimIndexes
        self.orginalDataLength = orginalDataLength

        self.b = 0
        self.a = 0
        self.x = 1
        self.regresyonModal = 0

    def calculateRegresyon(self):
        self.regresyonDecider()
        # self.testVerileriAdd()
        self.bCalculator()
        self.aCalculator()
        self.calculateTahminiValue()
        self.calculateTestTahminiValue()

        # print(self.b)
        # print(self.a)

    def regresyonDecider(self):
        # r'ye gore x belirleyici
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.selectedData = self.datas['X1']
        else:
            self.selectedData = self.datas['X2']

    def regresyonGetSelectedData(self):
        return self.selectedData

    def bCalculator(self):
        self.b = float("%.2f" % (((self.n * self.selectedData["sumOfXY"]) - (self.selectedData["sumOfX"] * self.datas['Y']["sumOfY"])) / (self.n * self.selectedData["sumSquareOfX"] - (self.selectedData["sumOfX"]) ** 2)))

    def aCalculator(self):
        self.a = float("%.2f" % (self.datas['Y']['avgY'] - (float(self.b) * float(self.selectedData['avgX']))))

    def calculateTestTahminiValue(self):
        for index in range(len(self.selectedData['X_TEST_VERILERI'])):
            self.selectedData['y^(Test Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_TEST_VERILERI'][index]))))

    def calculateTahminiValue(self):
        for index in range(self.n):
            self.selectedData['y^(Egitim Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['xValues'][index]))))
            # self.datas['X']['X_EGITIM_VERILERI'].append(float("%.2f" % (self.a + (self.b * self.selectedData['xValues'][index]))))

            # self.tahminiValues.append(self.a + (self.b * self.selectedData['xValues'][index]))


class Regresyon2():  # Formulas#):
    # def __init__(self, formulas, n, reklam, telefon, satislar):
    #     super(Regresyon, self).__init__(reklam, telefon, satislar)
    def __init__(self, formulas, columnCount):

        self.n = len(formulas.deneme['X1']['X_EGITIM_VALUES'])
        self.selectedData = {}
        self.datas = formulas.deneme
        self.columnCount = columnCount

        self.b = 0
        self.a = 0
        self.x = 1

    def calculateRegresyon(self):
        self.regresyonDecider()
        # self.testVerileriAdd()
        self.bCalculator()
        self.aCalculator()
        self.calculateTahminiValue()
        self.calculateTestTahminiValue()

        # print(self.b)
        # print(self.a)

    def regresyonDecider(self):
        maxR = self.datas['X1']['r1']  # en kötu zaten 1 zate x1 olacak o yuzden x1'i baslangicta max olarak alıyorum

        for index in range(1, self.columnCount - 1):
            key = ('X' + str(index))
            r = ('r') + str(index)

            if maxR < self.datas[key][r]:
                self.selectedData = self.datas[key][r]

        # r'ye gore x belirleyici
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.selectedData = self.datas['X1']
        else:
            self.selectedData = self.datas['X2']

    def regresyonGetSelectedData(self):
        return self.selectedData

    def bCalculator(self):
        self.b = float("%.2f" % (((self.n * self.selectedData["sumOfXY"]) - (self.selectedData["sumOfX"] * self.datas['Y']["sumOfY"])) / (self.n * self.selectedData["sumSquareOfX"] - (self.selectedData["sumOfX"]) ** 2)))

    def aCalculator(self):
        print(self.datas['Y']['avgY'])
        print(self.b)
        print(float(self.selectedData['avgX']))
        self.a = float("%.2f" % (self.datas['Y']['avgY'] - (float(self.b) * float(self.selectedData['avgX']))))

    def calculateTestTahminiValue(self):
        for index in range(len(self.selectedData['X_TEST_VALUES'])):
            self.selectedData['y^(Test Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_TEST_VALUES'][index]))))

    def calculateTahminiValue(self):
        for index in range(self.n):
            self.selectedData['y^(Egitim Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_EGITIM_VALUES'][index]))))
            # self.datas['X']['X_EGITIM_VERILERI'].append(float("%.2f" % (self.a + (self.b * self.selectedData['xValues'][index]))))

            # self.tahminiValues.append(self.a + (self.b * self.selectedData['xValues'][index]))


class SSE():
    # def __init__(self, korelasyon, formulas, n):
    def __init__(self, formulas, regresyon, n):

        self.formula = formulas
        self.n = n
        self.datas = formulas.getDatas()
        # self.datas = korelasyon.getDatas()
        self.selectedData = regresyon.regresyonGetSelectedData()

    def calculateEgitimVerilerSSE(self):
        sum = 0
        for yi in range(self.n):
            # sum += (self.datas['Y']['Y_VALUES'][yi] - self.datas['Y']['y^(Egitim Tahmini Degerler)'][yi]) ** 2
            sum += (self.datas['Y']['Y_VALUES'][yi] - self.selectedData['y^(Egitim Tahmini Degerler)'][yi]) ** 2

        print(float("%.3f" % (sum)))
        self.selectedData['SSE_EGITIM'] = float("%.3f" % (sum))

    def calculateTestVerilerSSE(self):
        sum = 0
        print(self.selectedData['X_TEST_VERILERI'])
        for yi in range(len(self.selectedData['X_TEST_VERILERI'])):
            sum += (self.datas['Y']['Y_TEST_VERILERI'][yi] - self.selectedData['X_TEST_VERILERI'][yi]) ** 2
        print(float("%.3f" % (sum)))
        self.selectedData['SSE_TEST'] = float("%.3f" % (sum))


class SSE2():
    # def __init__(self, korelasyon, formulas, n):
    def __init__(self, formulas, regresyon):

        self.n = len(formulas.deneme['X1']['X_EGITIM_VALUES'])
        self.datas = formulas.deneme
        self.selectedData = regresyon.regresyonGetSelectedData()

    def calculateEgitimVerilerSSE(self):
        sum = 0
        for yi in range(self.n):
            # sum += (self.datas['Y']['Y_VALUES'][yi] - self.datas['Y']['y^(Egitim Tahmini Degerler)'][yi]) ** 2
            sum += (self.datas['Y']['Y_VALUES'][yi] - self.selectedData['y^(Egitim Tahmini Degerler)'][yi]) ** 2

        # print(float("%.3f" % (sum)))
        self.selectedData['SSE_EGITIM'] = float("%.3f" % (sum))

    def calculateTestVerilerSSE(self):
        sum = 0
        for yi in range(len(self.selectedData['X_TEST_VALUES'])):
            sum += (self.datas['Y']['Y_VALUES'][yi] - self.selectedData['y^(Test Tahmini Degerler)'][yi]) ** 2
        # print(float("%.3f" % (sum)))
        self.selectedData['SSE_TEST'] = float("%.3f" % (sum))


def egitimTestAyrimi(formuller3, columnCount):
    reklamHarcamalariEgitim = []
    telefonAramaSayilariEgitim = []
    satislarEgitim = []

    reklamHarcamalariTest = []
    telefonAramaSayilariTest = []
    satislarTest = []

    # x1 x2 xi fark etmez hepsinin uzunlugu(satir) ayni olmak zorunda
    egitimValueIndexCount = round(len(formuller3.deneme['X1']['X_VALUES']) * 0.7)
    rndNumbers = random.sample(range(0, len(formuller3.deneme['X1']['X_VALUES'])), egitimValueIndexCount)
    print(rndNumbers)
    uzunluk = len(formuller3.deneme['X1']['X_VALUES'])

    for index in range(uzunluk):
        for dictIndex in range(1, columnCount):
            if index in rndNumbers:
                if dictIndex == columnCount - 1:
                    key = ('Y')
                    formuller3.deneme[key]['Y_EGITIM_VALUES'].append(formuller3.deneme[key]['Y_VALUES'][index])
                else:
                    key = ('X' + str(dictIndex))
                    formuller3.deneme[key]['X_EGITIM_VALUES'].append(formuller3.deneme[key]['X_VALUES'][index])

            else:
                if dictIndex == columnCount - 1:
                    key = ('Y')
                    formuller3.deneme[key]['Y_TEST_VALUES'].append(formuller3.deneme[key]['Y_VALUES'][index])
                else:
                    key = ('X' + str(dictIndex))
                    formuller3.deneme[key]['X_TEST_VALUES'].append(formuller3.deneme[key]['X_VALUES'][index])
    return rndNumbers


def setFormulas(formuller3, columnCount):
    for index in range(1, columnCount):
        # y
        if index == columnCount - 1:
            key = ('Y')

            # formuller3.deneme[key]['y^(Egitim Tahmini Degerler)'] = []
            formuller3.deneme[key]['avgY'] = formuller3.getAvg(formuller3.deneme[key]['Y_EGITIM_VALUES'])
            formuller3.deneme[key]['sumOfY'] = formuller3.sum(formuller3.deneme[key]['Y_EGITIM_VALUES'])
            # formuller3.deneme[key]['sumOfXY'] = formuller3.sumOfXY(formuller3.deneme[key]['Y_EGITIM_VALUES'])
            formuller3.deneme[key]['sumSquareOfY'] = formuller3.sumOfSquare(formuller3.deneme[key]['Y_EGITIM_VALUES'])
            formuller3.deneme[key]['avgSquareOfY'] = formuller3.avgSquare(formuller3.deneme[key]['Y_EGITIM_VALUES'])

        # x
        else:
            key = ('X' + str(index))

            # formuller3.deneme[key]['y^(Egitim Tahmini Degerler)'] = []
            formuller3.deneme[key]['avgX'] = formuller3.getAvg(formuller3.deneme[key]['X_EGITIM_VALUES'])
            formuller3.deneme[key]['sumOfX'] = formuller3.sum(formuller3.deneme[key]['X_EGITIM_VALUES'])
            formuller3.deneme[key]['sumOfXY'] = formuller3.sumOfXY(formuller3.deneme[key]['X_EGITIM_VALUES'], formuller3.deneme['Y']['Y_EGITIM_VALUES'])
            formuller3.deneme[key]['sumSquareOfX'] = formuller3.sumOfSquare(formuller3.deneme[key]['X_EGITIM_VALUES'])
            formuller3.deneme[key]['avgSquareOfX'] = formuller3.avgSquare(formuller3.deneme[key]['X_EGITIM_VALUES'])
            formuller3.deneme[key]['SSE_EGITIM'] = []
            formuller3.deneme[key]['SSE_TEST'] = []


def main():

    formuller3 = Formulas({}, {}, {}, reklamTest={}, telefonTest={}, satislarTest={})

    excel = ExcelTo()
    excel.readDataFromExcel()
    columnCount = len(excel.dataFrame.columns)

    rawData = []

    # x1 1.indexten baslar. sonuncu colunmn her zaman y olacaktir.
    for index in range(1, columnCount):
        columnName = excel.dataFrame.columns[index]
        rawData = excel.convertToList(excel.dataFrame[columnName])

        # y
        if index == columnCount - 1:
            key = ('Y')
            formuller3.deneme[key] = {}
            formuller3.deneme[key][key] = columnName
            formuller3.deneme[key]['Y_VALUES'] = rawData
            formuller3.deneme[key]['Y_EGITIM_VALUES'] = []
            formuller3.deneme[key]['Y_TEST_VALUES'] = []

        # x
        else:
            key = ('X' + str(index))
            formuller3.deneme[key] = {}
            formuller3.deneme[key][key] = columnName
            formuller3.deneme[key]['X_VALUES'] = rawData
            formuller3.deneme[key]['X_EGITIM_VALUES'] = []
            formuller3.deneme[key]['X_TEST_VALUES'] = []
            formuller3.deneme[key]['y^(Test Tahmini Degerler)'] = []
            formuller3.deneme[key]['y^(Egitim Tahmini Degerler)'] = []

    yoxd = egitimTestAyrimi(formuller3, columnCount)
    formuller3.n = len(formuller3.deneme['X1']['X_EGITIM_VALUES'])

    # exceldekine gore test yapma yeri !! ! ! ! ! !
    formuller3.deneme['X1']['X_EGITIM_VALUES'] = [100, 112, 115, 117, 116, 120, 121, 117]
    formuller3.deneme['Y']['Y_EGITIM_VALUES'] = [5.5, 6, 5.9, 6.2, 6.3, 6.6, 6.4, 6.7]
    formuller3.deneme['X1']['X_TEST_VALUES'] = [110, 118, 120, 123]
    formuller3.deneme['Y']['Y_TEST_VALUES'] = [5.8, 6.5, 6.5, 6.8]

    setFormulas(formuller3, columnCount)

    korelasyon2 = Korelasyon2(formuller3, columnCount)
    korelasyon2.setKorelasyon()
    regresyon2 = Regresyon2(formulas=formuller3, columnCount=columnCount)
    regresyon2.calculateRegresyon()
    sse2 = SSE2(formulas=formuller3, regresyon=regresyon2)
    sse2.calculateEgitimVerilerSSE()
    sse2.calculateTestVerilerSSE()
    print(formuller3.deneme['X1'], end="\n")
    print(formuller3.deneme['X2'], end="\n")
    print(formuller3.deneme['Y'], end="\n")

    ###############################################
    return

    reklamHarcamalari = excel.convertToList(excel.dataFrame["Reklam Harcamaları(x)"])
    telefonAramaSayilari = excel.convertToList(excel.dataFrame["Telefon İle Arama Sayısı"])
    satislar = excel.convertToList(excel.dataFrame["Satışlar(USD)"])
    # %70 egitim %30 test verisi olacak sekilde ayarlanmali yani rastgele secicez. islemler egitim verisinden olacak
    # burda karma islemini hallederim liste uzerinden.

    reklamHarcamalariEgitim = []
    telefonAramaSayilariEgitim = []
    satislarEgitim = []

    reklamHarcamalariTest = []
    telefonAramaSayilariTest = []
    satislarTest = []

    egitimValueIndexCount = round(len(reklamHarcamalari) * 0.7)
    rndNumbers = random.sample(range(0, len(reklamHarcamalari)), egitimValueIndexCount)

    rndNumbers = yoxd
    # testValueIndex
    for index in range(len(reklamHarcamalari)):
        if index in rndNumbers:

            reklamHarcamalariEgitim.append(reklamHarcamalari[index])
            telefonAramaSayilariEgitim.append(telefonAramaSayilari[index])
            satislarEgitim.append(satislar[index])
        else:
            reklamHarcamalariTest.append(reklamHarcamalari[index])
            telefonAramaSayilariTest.append(telefonAramaSayilari[index])
            satislarTest.append(satislar[index])

    formuller = Formulas(reklamHarcamalariEgitim, telefonAramaSayilariEgitim, satislarEgitim, reklamTest=reklamHarcamalariTest, telefonTest=telefonAramaSayilariTest, satislarTest=satislarTest)
    formuller.setDatas()

    # korelasyon = Korelasyon(formuller, formuller.n, reklamHarcamalari, telefonAramaSayilari, satislar)
    korelasyon = Korelasyon(formuller, formuller.n)
    korelasyon.setKorelasyon()
    # regrasyon = Regresyon(formuller, formuller.n, reklamHarcamalari, telefonAramaSayilari, satislar)
    regresyon = Regresyon(formuller, formuller.n, rndNumbers, len(reklamHarcamalari))
    regresyon.calculateRegresyon()

    # sse = SSE(formuller, formuller.n)
    # sse = SSE(korelasyon, regresyon, formuller.n)
    sse = SSE(formuller, regresyon, formuller.n)

    sse.calculateEgitimVerilerSSE()
    sse.calculateTestVerilerSSE()
    print(formuller.datas["X1"], end="\n")
    print(formuller.datas["X2"], end="\n")
    print(formuller.datas["Y"], end="\n")


if __name__ == "__main__":
    main()
