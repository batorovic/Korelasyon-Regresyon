import random  # istenilen aralikta birbirinden farkli sayilar uretebilmek icin kullanilmistir


class Datas():
    def __init__(self, columnCount):
        self.datas = {}
        self.columnCount = columnCount

    def getDatas(self):
        return self.datas

    # excel'de istenildigi kadar x eklenebilecek, dinamik veri yapisinin olusturulma islemi
    def createDataKeysAndValues(self, excel):
        # x1'in 2. sutundan basladigi kabul edildigi icin dongu 1 den baslamistir. Ilk satir pass gecilmistir.
        for index in range(1, self.columnCount):
            columnName = excel.dataFrame.columns[index]
            rawData = excel.convertToList(excel.dataFrame[columnName])

            # y -> son sutun y olarak kabul edilmistir
            if index == self.columnCount - 1:
                key = ('Y')
                self.datas[key] = {}
                self.datas[key][key] = columnName
                self.datas[key]['Y_VALUES'] = rawData
                self.datas[key]['Y_EGITIM_VALUES'] = []
                self.datas[key]['Y_TEST_VALUES'] = []

            # x1,x2,x3,...,xn -> 1. sutun ile son sutun arasinda kalan sutunlar x olarak alinmistir.
            else:
                key = ('X' + str(index))
                self.datas[key] = {}
                self.datas[key][key] = columnName
                self.datas[key]['X_VALUES'] = rawData
                self.datas[key]['X_EGITIM_VALUES'] = []
                self.datas[key]['X_TEST_VALUES'] = []
                self.datas[key]['y^(Test Tahmini Degerler)'] = []
                self.datas[key]['y^(Egitim Tahmini Degerler)'] = []
                # self.datas[key]['SSE_EGITIM'] = []
                # self.datas[key]['SSE_TEST'] = []

    def egitimTestAyrimi(self):

        egitimValueIndexCount = round(len(self.datas['X1']['X_VALUES']) * 0.7)  # x1, x2, xi fark etmez hepsinin uzunlugu(sati sayisi) ayni olmaktadir
        # satir sayisi kadar rastgele birbirinden farkli sayilar uretilmistir
        rndNumbers = random.sample(range(0, len(self.datas['X1']['X_VALUES'])), egitimValueIndexCount)
        length = len(self.datas['X1']['X_VALUES'])

        # 1.for satir sayisina kadar 2. for ise sutun sayisi kadar islemekte
        for index in range(length):
            for dictIndex in range(1, self.columnCount):
                # Secilmis rastgele sayilarin icinde en son satira kadar giden indexlerden var ise bunlar egitim verileri olarak alindi. Yok ise test verileri olarak alindi(%30 luk kismi)
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

    # Gerekli olan degerler ilgili yerlere atanmistir
    def setFormulas(self, formuller):
        for index in range(1, self.columnCount):
            # y
            if index == self.columnCount - 1:
                key = ('Y')
                # formuller.datas[key]['y^(Egitim Tahmini Degerler)'] = []
                self.datas[key]['avgY'] = formuller.getAvg(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['sumOfY'] = formuller.sum(self.datas[key]['Y_EGITIM_VALUES'])
                # self.datas[key]['sumOfXY'] = formuller.sumOfXY(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['sumSquareOfY'] = formuller.sumOfSquare(self.datas[key]['Y_EGITIM_VALUES'])
                self.datas[key]['avgSquareOfY'] = formuller.avgSquare(self.datas[key]['Y_EGITIM_VALUES'])

            # x
            else:
                key = ('X' + str(index))

                # self.datas[key]['y^(Egitim Tahmini Degerler)'] = []
                self.datas[key]['avgX'] = formuller.getAvg(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['sumOfX'] = formuller.sum(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['sumOfXY'] = formuller.sumOfXY(self.datas[key]['X_EGITIM_VALUES'], self.datas['Y']['Y_EGITIM_VALUES'])
                self.datas[key]['sumSquareOfX'] = formuller.sumOfSquare(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['avgSquareOfX'] = formuller.avgSquare(self.datas[key]['X_EGITIM_VALUES'])
                self.datas[key]['SSE_EGITIM'] = []
                self.datas[key]['SSE_TEST'] = []
