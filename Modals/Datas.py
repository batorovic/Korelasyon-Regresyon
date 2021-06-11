import random


class Datas():
    def __init__(self, columnCount):
        self.datas = {}
        self.columnCount = columnCount

    def getDatas(self):
        return self.datas

    def createDataKeysAndValues(self, excel):
        for index in range(1, self.columnCount):
            columnName = excel.dataFrame.columns[index]
            rawData = excel.convertToList(excel.dataFrame[columnName])

            # y
            if index == self.columnCount - 1:
                key = ('Y')
                self.datas[key] = {}
                self.datas[key][key] = columnName
                self.datas[key]['Y_VALUES'] = rawData
                self.datas[key]['Y_EGITIM_VALUES'] = []
                self.datas[key]['Y_TEST_VALUES'] = []

            # x
            else:
                key = ('X' + str(index))
                self.datas[key] = {}
                self.datas[key][key] = columnName
                self.datas[key]['X_VALUES'] = rawData
                self.datas[key]['X_EGITIM_VALUES'] = []
                self.datas[key]['X_TEST_VALUES'] = []
                self.datas[key]['y^(Test Tahmini Degerler)'] = []
                self.datas[key]['y^(Egitim Tahmini Degerler)'] = []

    def egitimTestAyrimi(self):
        # x1 x2 xi fark etmez hepsinin uzunlugu(satir) ayni olmak zorunda
        egitimValueIndexCount = round(len(self.datas['X1']['X_VALUES']) * 0.7)
        rndNumbers = random.sample(range(0, len(self.datas['X1']['X_VALUES'])), egitimValueIndexCount)
        print(rndNumbers)
        uzunluk = len(self.datas['X1']['X_VALUES'])

        for index in range(uzunluk):
            for dictIndex in range(1, self.columnCount):
                if index in rndNumbers:
                    if dictIndex == self.columnCount - 1:
                        key = ('Y')
                        self.datas[key]['Y_EGITIM_VALUES'].append(self.datas[key]['Y_VALUES'][index])
                    else:
                        key = ('X' + str(dictIndex))
                        self.datas[key]['X_EGITIM_VALUES'].append(self.datas[key]['X_VALUES'][index])

                else:
                    if dictIndex == self.columnCount - 1:
                        key = ('Y')
                        self.datas[key]['Y_TEST_VALUES'].append(self.datas[key]['Y_VALUES'][index])
                    else:
                        key = ('X' + str(dictIndex))
                        self.datas[key]['X_TEST_VALUES'].append(self.datas[key]['X_VALUES'][index])
        # return rndNumbers

    def setFormulas(self, formuller3):
        for index in range(1, self.columnCount):
            # y
            if index == self.columnCount - 1:
                key = ('Y')
                # formuller3.datas[key]['y^(Egitim Tahmini Degerler)'] = []
                self.datas[key]['avgY'] = formuller3.getAvg(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['sumOfY'] = formuller3.sum(self.datas[key]['Y_EGITIM_VALUES'])
                # self.datas[key]['sumOfXY'] = formuller3.sumOfXY(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['sumSquareOfY'] = formuller3.sumOfSquare(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['avgSquareOfY'] = formuller3.avgSquare(self.datas[key]['Y_EGITIM_VALUES'])

            # x
            else:
                key = ('X' + str(index))

                # self.datas[key]['y^(Egitim Tahmini Degerler)'] = []
                self.datas[key]['avgX'] = formuller3.getAvg(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['sumOfX'] = formuller3.sum(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['sumOfXY'] = formuller3.sumOfXY(self.datas[key]['X_EGITIM_VALUES'], self.datas['Y']['Y_EGITIM_VALUES'])
                self.datas[key]['sumSquareOfX'] = formuller3.sumOfSquare(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['avgSquareOfX'] = formuller3.avgSquare(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['SSE_EGITIM'] = []
                self.datas[key]['SSE_TEST'] = []
