import backtrader as bt
import datetime

class FVGStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if self.order:
            return

        # Bullish FVG Setup 
        if len(self) >= 3:
            bullish_fvg = self.datalow[0] > self.datahigh[-2] and self.dataclose[-1] > self.datahigh[-2]
            
            if not self.position:
                if bullish_fvg:
                    self.log('Bullish FVG ગેપ મળ્યો, BUY ENTRY')
                    self.order = self.buy()
            else:
                if len(self) >= (self.bar_executed + 3):
                    self.log('ટ્રેડ ક્લોઝ કર્યો')
                    self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(FVGStrategy)

    # GitHub પર ટેસ્ટ કરવા માટે ફેક ડેટા જનરેટ કર્યો છે 
    data = bt.feeds.YahooFinanceData(
        dataname='EURUSD=X',
        fromdate=datetime.datetime(2023, 1, 1),
        todate=datetime.datetime(2023, 12, 31),
        reverse=False)
    
    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    
    print('શરૂઆતનું બેલેન્સ: $%.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('અંતિમ બેલેન્સ: $%.2f' % cerebro.broker.getvalue())
