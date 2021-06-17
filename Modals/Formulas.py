# Korelasyon, regresyon islemlerinde lazim olacak degerlerin hesaplanmasini saglayan fonksiyonlari barindiran class
class Formulas():
    def __init__(self):
        self._n = 0
        self.datas = {}

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        self._n = n

    def getAvg(self, data):
        sum = 0
        for item in data:
            sum += item
        return sum / self.n

    def sum(self, data):
        sum = 0
        for item in data:
            sum += item
        return sum

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
