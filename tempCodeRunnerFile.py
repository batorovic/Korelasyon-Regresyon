
        self.x1 = {'x1': 'Reklam', 'avgX1': self.getAvg(reklam), 'sumOfX1Y': self.sumOfXY(reklam, satislar), 'sumOfSquareX1': self.sumOfSquare(reklam), 'r1': self.korelasyonCalculator(reklam)}

        self.x2 = {'x2': 'Telefon', 'avgX2': self.getAvg(telefon), 'sumOfX2Y': self.sumOfXY(telefon, satislar), 'sumOfSquareX2': self.sumOfSquare(telefon), 'r2': self.korelasyonCalculator(telefon)}

        self.rData = self.korelasyonDecider()

    def korelasyonCalculator(self, data):

        return (self.x1['sumofX1Y'] - self.n * self.x1['avgX1']*self.x2['avgX2']) / 8

    def korelasyonDecider(self):