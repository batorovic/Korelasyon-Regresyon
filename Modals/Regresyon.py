class Regresyon2():
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

    def calculateEgitimTahminiValue(self):
        for index in range(self.n):
            self.selectedData['y^(Egitim Tahmini Degerler)'].append(float("%.2f" % (self.a + (self.b * self.selectedData['X_EGITIM_VALUES'][index]))))

    def insertRegresyonDenklemiToSelectedDict(self):
        self.selectedData['Regresyon Denklemi'] = 'y^ = a + bx -> y^ = ' + str(self.a)+' + '+str(self.b)+'x'
