import pandas as pd


class ExcelTo:
    def __init__(self):
        self.dataFrame = 0
        self.liste = []

    def readDataFromExcel(self):
        self.dataFrame = pd.read_excel(r"veriSeti.xlsx", keep_default_na=False)
        # Excel dosyasini scriptin oldugu yerden direkt okumaktadir.

        # excelden columnlari okuyunca bos olan columnlar unnamed olarak geliyor onlari silme islemi.
        self.dataFrame = self.dataFrame.loc[:, ~self.dataFrame.columns.str.contains('^Unnamed')]

    # excel'den okunan verileri listeye cevirme islemi
    def convertToList(self, data):
        self.liste = []

        for item in data:
            if item == "":
                break
            else:
                self.liste.append(item)
        return self.liste

    def getColumnCount(self):
        return len(self.dataFrame.columns)
