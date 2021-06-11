class SSE2():
    def __init__(self, dictData, regresyon):
        self.n = len(dictData.getDatas()['X1']['X_EGITIM_VALUES'])
        self.datas = dictData.getDatas()
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
