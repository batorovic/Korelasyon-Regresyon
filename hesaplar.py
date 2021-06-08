import math
from numpy import index_exp, select
import pandas as pd


class ExcelTo:
    def __init__(self):
        self.dataFrame = 0
        self.liste = []

    def readDataFromExcel(self):
        self.dataFrame = pd.read_excel(r"veriSeti.xlsx", keep_default_na=False)
        # Excel dosyasini scriptin oldugu yerden direkt okumaktadir.
        # return self.dataFrame

    def convertToList(self, data):
        self.liste = []

        for item in data:
            if item == "":
                break
            else:
                self.liste.append(item)
        return self.liste


class Formulas():
    def __init__(self, reklam, telefon, satislar):
        self.n = len(satislar)  # hepsinin uzunlugu aynı olacagi icin 1 tanesinin lenini almak yeterli.
        self.rData = 0
        self.reklam = reklam
        self.telefon = telefon
        self.satislar = satislar
        self.datas = {}

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
                'xValues': self.reklam,
                'avgX': self.getAvg(self.reklam),
                'sumOfX': self.sum(self.reklam),
                'sumOfXY': self.sumOfXY(self.reklam, self.satislar),
                'sumSquareOfX': self.sumOfSquare(self.reklam),
                'avgSquareOfX': self.avgSquare(self.reklam),
            },
            'X2': {
                'x2': 'Telefon',
                'xValues': self.telefon,
                'avgX': self.getAvg(self.telefon),
                'sumOfX': self.sum(self.telefon),
                'sumOfXY': self.sumOfXY(self.telefon, self.satislar),
                'sumSquareOfX': self.sumOfSquare(self.telefon),
                'avgSquareOfX': self.avgSquare(self.telefon),
            },
            'Y': {
                'Y': 'Satislar',
                'y^(Egitim Tahmini Degerler)': [],
                'y^(Test Tahmini Degerler)': [],
                'Y_VALUES': self.satislar,
                'avgY': self.getAvg(self.satislar),
                'sumOfY': self.sum(self.satislar),
                'sumSquareOfY': self.sumOfSquare(self.satislar),
                'avgSquareOfY': self.avgSquare(self.satislar),
            }
        }

    def getDatas(self):
        return self.datas


# class Korelasyon(Formulas):
#     def __init__(self, formulas, n, reklam, telefon, satislar):
#         super(Korelasyon, self).__init__(reklam, telefon, satislar)
#         self.n = n
#         self.datas = formulas.getDatas()
#         self.formuller = formulas

#     def setKorelasyon(self):
#         self.datas['X1']['r1'] = "%0.5f" % (self.korelasyonCalculator("X1"))
#         self.datas['X2']['r2'] = "%0.5f" % (self.korelasyonCalculator("X2"))
#         self.korelasyonDecider()

#     def korelasyonCalculator(self, data):
#         return (self.datas[data]['sumOfXY'] - self.n * self.datas[data]['avgX']*self.datas['Y']['avgY']) / math.sqrt((self.datas[data]['sumSquareOfX'] - self.n*self.datas[data]['avgSquareOfX']) * ((self.datas['Y']['sumSquareOfY'] - self.n*self.datas['Y']['avgSquareOfY'])))

#     def korelasyonDecider(self):
#         if self.datas['X1']['r1'] > self.datas['X2']['r2']:
#             self.rData = self.datas['X1']['r1']
#         else:
#             self.rData = self.datas['X2']['r2']

class Korelasyon(Formulas):
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

    def korelasyonDecider(self):
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.rData = self.datas['X1']['r1']
        else:
            self.rData = self.datas['X2']['r2']


class Regresyon():  # Formulas#):
    # def __init__(self, formulas, n, reklam, telefon, satislar):
    #     super(Regresyon, self).__init__(reklam, telefon, satislar)
    def __init__(self, formulas, n):

        self.formula = formulas
        self.n = n
        self.selectedData = {}
        self.datas = formulas.getDatas()

        self.b = 0
        self.a = 0
        self.x = 1
        self.regresyonModal = 0

    def calculateRegresyon(self):
        self.regresyonDecider()
        self.bCalculator()
        self.aCalculator()
        self.calculateTahminiValue()

        # print(self.b)
        # print(self.a)

    def bCalculator(self):
        self.b = float("%.2f" % (((self.n * self.selectedData["sumOfXY"]) - (self.selectedData["sumOfX"] * self.datas['Y']["sumOfY"])) / (self.n * self.selectedData["sumSquareOfX"] - (self.selectedData["sumOfX"]) ** 2)))

    def aCalculator(self):
        self.a = float("%.2f" % (self.datas['Y']['avgY'] - (float(self.b) * float(self.selectedData['avgX']))))

    def regresyonDecider(self):
        # r'ye gore x belirleyici
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.selectedData = self.datas['X1']
        else:
            self.selectedData = self.datas['X2']

    def calculateTahminiValue(self):
        for index in range(self.n):
            self.datas['Y']['y^(Egitim Tahmini Degerler)'].append(self.a + (self.b * self.selectedData['xValues'][index]))
            # self.tahminiValues.append(self.a + (self.b * self.selectedData['xValues'][index]))


class SSE():
    def __init__(self, formulas, n):
        self.formula = formulas
        self.n = n
        self.datas = formulas.getDatas()

    def calculateEgitimVerilerSSE(self):
        sum = 0
        for yi in range(self.n):
            sum += (self.datas['Y']['Y_VALUES'][yi] - self.datas['Y']['y^(Egitim Tahmini Degerler)'][yi]) ** 2
        print(float("%.3f" % (sum)))

    def calculateTestVerilerSSE(self):
        sum = 0
        for yi in range(self.n):
            sum += (self.datas['Y']['Y_VALUES'][yi] - self.datas['Y']['y^(Test Tahmini Degerler)'][yi]) ** 2
        print(float("%.3f" % (sum)))


def main():

    excel = ExcelTo()
    excel.readDataFromExcel()

    reklamHarcamalari = excel.convertToList(excel.dataFrame["Reklam Harcamaları(x)"])
    telefonAramaSayilari = excel.convertToList(excel.dataFrame["Telefon İle Arama Sayısı"])
    satislar = excel.convertToList(excel.dataFrame["Satışlar(USD)"])
    # %70 egitim %30 test verisi olacak sekilde ayarlanmali yani rastgele secicez. islemler egitim verisinden olacak
    # burda karma islemini hallederim liste uzerinden.

    formuller = Formulas(reklamHarcamalari, telefonAramaSayilari, satislar)
    formuller.setDatas()
    # korelasyon = Korelasyon(formuller, formuller.n, reklamHarcamalari, telefonAramaSayilari, satislar)
    korelasyon = Korelasyon(formuller, formuller.n)
    korelasyon.setKorelasyon()
    # regrasyon = Regresyon(formuller, formuller.n, reklamHarcamalari, telefonAramaSayilari, satislar)
    regresyon = Regresyon(formuller, formuller.n)
    regresyon.calculateRegresyon()

    sse = SSE(formuller, formuller.n)
    sse.calculateEgitimVerilerSSE()

    print(formuller.datas["X1"])
    print(formuller.datas["X2"])
    print(formuller.datas["Y"])


if __name__ == "__main__":
    main()
