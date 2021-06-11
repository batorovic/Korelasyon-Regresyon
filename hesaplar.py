from Modals.ExcelTo import ExcelTo
from Modals.Datas import Datas
from Modals.Formulas import Formulas
from Modals.Korelasyon import Korelasyon2
from Modals.Regresyon import Regresyon2
from Modals.SumOfSquaredError import SSE2


class PrintToScreen():
    def __init__(self, dataDict):
        self.dataDict = dataDict

    def printDatas(self):
        # for key, data in self.dataDict.items():
        #     print(key)
        #     for attribute, value in data.items():
        #         print('{} : {}'.format(attribute, value))

        for key, value in self.dataDict.items():
            print('{} : {}'.format(key, value))


def main():

    formuller3 = Formulas()

    excel = ExcelTo()
    excel.readDataFromExcel()
    columnCount = len(excel.dataFrame.columns)

    datas = Datas(columnCount=columnCount)
    datas.createDataKeysAndValues(excel=excel)
    datas.egitimTestAyrimi()
    dataDict = datas.getDatas()

    formuller3.n = len(dataDict['X1']['X_EGITIM_VALUES'])

    # exceldekine gore test yapma yeri !! ! ! ! ! ! #ornek veriler
    # dataDict['X1']['X_EGITIM_VALUES'] = [100, 112, 115, 117, 116, 120, 121, 117]
    # dataDict['Y']['Y_EGITIM_VALUES'] = [5.5, 6, 5.9, 6.2, 6.3, 6.6, 6.4, 6.7]
    # dataDict['X1']['X_TEST_VALUES'] = [110, 118, 120, 123]
    # dataDict['Y']['Y_TEST_VALUES'] = [5.8, 6.5, 6.5, 6.8]

    datas.setFormulas(formuller3=formuller3)

    korelasyon2 = Korelasyon2(dictData=datas, columnCount=columnCount)
    korelasyon2.setKorelasyon()
    regresyon2 = Regresyon2(dictData=datas, columnCount=columnCount)
    regresyon2.calculateRegresyon()
    sse2 = SSE2(dictData=datas, regresyon=regresyon2)
    sse2.calculateEgitimVerilerSSE()
    sse2.calculateTestVerilerSSE()

    dataDict = regresyon2.regresyonGetSelectedData()
    printToScreen = PrintToScreen(dataDict=dataDict)
    printToScreen.printDatas()

    # print(dataDict['X1'], end="\n")
    # print(dataDict['X2'], end="\n")
    # print(dataDict['Y'], end="\n")


if __name__ == "__main__":
    main()
