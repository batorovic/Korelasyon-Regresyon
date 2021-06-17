r"""
Python 3.9.0 versiyonu kullanilmistir.

149 ulkenin Sosyal Destek ve Saglikli yasam belirtisine gore 0-10 arasinda ladder score'u bulunmaktadir. Bu verilere gore islemler yapilmistir.

Excelden veri okumak icin pandas ve openpyxl,
Sqrt fonksiyonunu kullanabilmek serbest oldugun icin math
kütüphaneleri kullanilmistir.

Kodun calismasi icin asagidaki kutuphaneleri pip ile yuklemeniz gerekmektedir.

pip install pandas
pip install openpyxl
pip install numpy (Pandas icin gereklidir. Pandas yuklenirken numpy da yukleniyor. Ama yuklenmez ise siz kurunuz.)

Eger pip hata verirse:

Ortam degiskenleri -> Sistem Degiskenleri -> Path

Path kismina: C: \Users\{kullaniciAdiniz}\AppData\Local\Programs\Python\Python39\Scripts yolunu ekleyiniz.

Scripti cmd uzerinden calistirmak isterseniz:

Dosyayi cikardiginiz yerde cmd aciniz. Ve asagidaki satiri yaziniz.

py hesaplamalar.py

"""

from Modals.ExcelTo import ExcelTo  # Excel'den okudugumuz verileri isledigimiz class

from Modals.Datas import Datas  # Verileri islerken dictionary olarak tutmak istedim. Bu class'da dictionary nin , key ve value'lari belirleniyor ayrica egitim, test ayrimi yapiliyor
from Modals.Formulas import Formulas  # Formullerde lazim olan toplama,ortalama, toplamin karesi vb fonksiyonlari iceren class dir
from Modals.Korelasyon import Korelasyon  # Korelasyon hesabinin yapildigi class
from Modals.Regresyon import Regresyon  # Regresyon hesabinin yapildigi class
from Modals.SumOfSquaredError import SSE  # Sum Of Squared Error hesabinin yapildigi class


def printDatas(selectedDataDict, dataDict, columnCount):
    print()

    for index in range(1, columnCount-1):
        r = ('r') + str(index)
        key = ('X' + str(index))
        print((key + '(' + dataDict[key][key] + '),' + r+' ='), dataDict[key][r])
        print()

    for key, value in selectedDataDict.items():
        print('{} : {}'.format(key, value))
        break

    print('{} : {}'.format('X EGITIM VERILERI', selectedDataDict['X_EGITIM_VALUES']), end="\n\n")
    print('{} : {}'.format('y^(Egitim Tahmini Degerler)', selectedDataDict['y^(Egitim Tahmini Degerler)']), end="\n\n")
    print('{} : {}'.format('Regresyon Denklemi', selectedDataDict['Regresyon Denklemi']), end="\n\n")
    print('{} : {}'.format('SSE Egitim', selectedDataDict['SSE_EGITIM']), end="\n\n")

    print('{} : {}'.format('X TEST VERILERI', selectedDataDict['X_TEST_VALUES']), end="\n\n")
    print('{} : {}'.format('y^(Test Tahmini Degerler)', selectedDataDict['y^(Test Tahmini Degerler)']), end="\n\n")
    print('{} : {}'.format('SSE TEST', selectedDataDict['SSE_TEST']), end="\n\n")


def main():
    formuller = Formulas()

    excel = ExcelTo()
    excel.readDataFromExcel()
    columnCount = excel.getColumnCount()

    datas = Datas(columnCount=columnCount)
    datas.createDataKeysAndValues(excel=excel)
    datas.egitimTestAyrimi()
    dataDict = datas.getDatas()

    formuller.n = len(dataDict['X1']['X_EGITIM_VALUES'])

    datas.setFormulas(formuller=formuller)

    korelasyon = Korelasyon(dictData=datas, columnCount=columnCount)
    korelasyon.setKorelasyon()
    regresyon = Regresyon(dictData=datas, columnCount=columnCount)
    regresyon.calculateRegresyon()
    sse = SSE(dictData=datas, regresyon=regresyon)
    sse.calculateEgitimVerilerSSE()
    sse.calculateTestVerilerSSE()

    selectedDataDict = regresyon.regresyonGetSelectedData()
    dataDict = datas.getDatas()

    printDatas(selectedDataDict=selectedDataDict, dataDict=dataDict, columnCount=columnCount)


if __name__ == "__main__":
    main()
