import math


class Korelasyon():
    def __init__(self, dictData, columnCount):
        self.n = len(dictData.getDatas()['X1']['X_EGITIM_VALUES'])  # fark etmez herhangi birinin egitim uzunlugu olabilir
        self.datas = dictData.getDatas()
        self.columnCount = columnCount

    # Her bir x icin korelasyon bulunmasi
    def setKorelasyon(self):
        for index in range(1, self.columnCount - 1):
            key = ('X' + str(index))
            r = ('r') + str(index)
            self.datas[key][r] = float("%0.5f" % (self.korelasyonCalculator(key)))

    # Korelasyonu bulmayi saglayan formulu iceren fonksiyon
    def korelasyonCalculator(self, key):
        # 0'a bolunememe durumu olabilir.
        try:
            return (self.datas[key]['sumOfXY'] - self.n * self.datas[key]['avgX']*self.datas['Y']['avgY']) / math.sqrt((self.datas[key]['sumSquareOfX'] - self.n*self.datas[key]['avgSquareOfX']) * ((self.datas['Y']['sumSquareOfY'] - self.n * self.datas['Y']['avgSquareOfY'])))
        except:
            return 0
