class Regresyon():
    def __init__(self, dictData, columnCount):

        self.n = len(dictData.getDatas()['X1']['X_EGITIM_VALUES'])
        self.selectedData = {}
        self.datas = dictData.getDatas()
        self.columnCount = columnCount

        self.b = 0
        self.a = 0
        self.x = 1

    def calculateRegresyon(self):
        self.regresyonDecider()
        # self.testVerileriAdd()
        self.bCalculator()
        self.aCalculator()
        self.calculateEgitimTahminiValue()
        self.calculateTestTahminiValue()
        self.insertRegresyonDenklemiToSelectedDict()

    def regresyonGetSelectedData(self):
        return self.selectedData

    def regresyonDecider(self):
        maxR = self.datas['X1']['r1']  # en kötu x1 olacak o yuzden x1'in r degerini baslangicta max olarak aliyorum
        self.selectedData = self.datas['X1']

        # Ne kadar x var ise onlarin r degerlerini karsilastiriyorum. En buyuk olani seciyorum
        for index in range(1, self.columnCount - 1):
            key = ('X' + str(index))
            r = ('r') + str(index)

            if maxR < self.datas[key][r]:
                self.selectedData = self.datas[key]
                maxR = self.datas[key][r]

    # Regresyonda degerinin bulunmasini saglayan formul
    def bCalculator(self):
        try:
            self.b = float("%.2f" % (((self.n * self.selectedData["sumOfXY"]) - (self.selectedData["sumOfX"] * self.datas['Y']["sumOfY"])) / (self.n * self.selectedData["sumSquareOfX"] - (self.selectedData["sumOfX"]) ** 2)))
        except:
            # 0'a bolunmeme durumunda b'yi 0'a esitledim
            self.b = 0

    # Regresyonda a degerinin bulunmasini saglayan formul
    def aCalculator(self):
        self.a = float("%.2f" % (self.datas['Y']['avgY'] - (float(self.b) * float(self.selectedData['avgX']))))

    # Test verileri icin tahmini deger bulunmasi
    def calculateTestTahminiValue(self):
        for index in range(len(self.selectedData['X_TEST_VALUES'])):
            self.selectedData['y^(Test Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_TEST_VALUES'][index]))))

    # Egitim verileri icin tahmini deger bulunmasi
    def calculateEgitimTahminiValue(self):
        for index in range(self.n):
            self.selectedData['y^(Egitim Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_EGITIM_VALUES'][index]))))
    # Ilgılı x in dictionary sine a ve b degerlerinin formulde gosterildi bilgi eklenmektedir

    def insertRegresyonDenklemiToSelectedDict(self):
        self.selectedData['Regresyon Denklemi'] = 'y^ = a + bx -> y^ = ' + str(self.a)+' + '+str(self.b)+'x'
