import math
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


class Formulas:
    def __init__(self, reklam, telefon, satislar):
        # self.x1 = reklam
        # self.x2 = telefon
        # self.y = satislar
        self.n = len(satislar)  # hepsinin uzunlugu aynı olacagi icin 1 tanesinin lenini almak yeterli.

        # self.avgX1 = self.getAvg(reklam)
        # self.avgX2 = self.getAvg(telefon)
        # self.avgY = self.getAvg(satislar)
        # self.sumOfX1Y = self.sumOfXY(reklam, satislar)
        # self.sumOfX2Y = self.sumOfXY(telefon, satislar)
        # self.r1 = self.korelasyonCalculator(reklam)
        # self.r2 = self.korelasyonCalculator(telefon)
        self.rData = 0

        self.datas = {
            "X1": {
                'x1': 'Reklam',
                'avgX': self.getAvg(reklam),
                'sumOfXY': self.sumOfXY(reklam, satislar),
                'sumSquareOfX': self.sumOfSquare(reklam),
                'avgSquareOfX': self.avgSquare(reklam),
                # 'r1': self.korelasyonCalculator('X1'),
            },
            'X2': {
                'x2': 'Telefon',
                'avgX': self.getAvg(telefon),
                'sumOfXY': self.sumOfXY(telefon, satislar),
                'sumSquareOfX': self.sumOfSquare(telefon),
                'avgSquareOfX': self.avgSquare(telefon),
                # 'r2': self.korelasyonCalculator('X2'),
            },
            'Y': {
                'Y': 'Satislar',
                'avgY': self.getAvg(satislar),
                'sumSquareOfY': self.sumOfSquare(satislar),
                'avgSquareOfY': self.avgSquare(satislar),
            },

        }

        # self.x2 = {'x2': 'Telefon', 'avgX2': self.getAvg(telefon), 'sumofX2Y': self.sumOfXY(telefon, satislar), 'sumOfSquareX2': self.sumOfSquare(telefon), 'r2': self.korelasyonCalculator(telefon)}

    def korelasyonCalculator(self, data):
        return (self.datas[data]['sumOfXY'] - self.n * self.datas[data]['avgX']*self.datas['Y']['avgY']) / math.sqrt((self.datas[data]['sumSquareOfX'] - self.n*self.datas[data]['avgSquareOfX']) * ((self.datas['Y']['sumSquareOfY'] - self.n*self.datas['Y']['avgSquareOfY'])))

    def korelasyonDecider(self):
        if self.datas['X1']['r1'] > self.datas['X2']['r2']:
            self.rData = self.datas['X1']['r1']
        else:
            self.rData = self.datas['X2']['r2']

    def getAvg(self, data):
        sum = 0
        for item in data:
            sum += item
        return sum / self.n

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


def main():

    excel = ExcelTo()
    excel.readDataFromExcel()

    reklamHarcamalari = excel.convertToList(excel.dataFrame["Reklam Harcamaları(x)"])
    telefonAramaSayilari = excel.convertToList(excel.dataFrame["Telefon İle Arama Sayısı"])
    satislar = excel.convertToList(excel.dataFrame["Satışlar(USD)"])

    formuller = Formulas(reklamHarcamalari, telefonAramaSayilari, satislar)
    formuller.datas['X1']['r1'] = "%0.5f" % (formuller.korelasyonCalculator("X1"))
    formuller.datas['X2']['r2'] = "%0.5f" % (formuller.korelasyonCalculator("X2"))
    # formuller.datas['X1'] = {
    #     'r1': "%0.5f" % (formuller.korelasyonCalculator("X1")),
    #     'r2': "%0.5f" % (formuller.korelasyonCalculator("X2")),
    # }
    formuller.korelasyonDecider()
    print(formuller.rData)
    print(formuller.datas['X1'], formuller.datas['X2'])


if __name__ == "__main__":
    main()
