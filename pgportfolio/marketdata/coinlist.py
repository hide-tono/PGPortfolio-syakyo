import logging
from datetime import datetime

import pandas as pd

from pgportfolio.marketdata.poloniex import Poloniex
from pgportfolio.tools.data import get_chart_until_success
from pgportfolio.trade.constants import DAY


class CoinList(object):
    def __init__(self, end, volume_average_days=1, volume_forward=0):
        self._polo = Poloniex()
        vol = self._polo.marketVolume()
        ticker = self._polo.marketTicker()
        pairs = []
        coins = []
        volumes = []
        prices = []

        logging.info("select coin online from %s to %s"
                     % (datetime.fromtimestamp(end - (DAY * volume_average_days) - volume_forward).strftime('%Y-%m-%d %H:%M'),
                        datetime.fromtimestamp(end - volume_forward).strftime('%Y-%m-%d %H:%M')))

        for k, v in vol.items():
            if k.startswith("BTC_") or k.endswith("_BTC"):
                pairs.append(k)
                for c, val in v.items():
                    if c != 'BTC':
                        if k.endswith('_BTC'):
                            # BTCが後ろなら逆数にする
                            coins.append('reversed_' + c)
                            prices.append(1.0 / float(ticker[k]['last']))
                        else:
                            coins.append(c)
                            prices.append(float(ticker[k]['last']))
                    else:
                        volumes.append(self.__get_total_volume(pair=k, global_end=end,
                                                               days=volume_average_days,
                                                               forward=volume_forward))
        self._df = pd.DataFrame({'coin': coins, 'pair': pairs, 'volume': volumes, 'price': prices})
        self._df = self._df.set_index('coin')

    def __get_total_volume(self, pair, global_end, days, forward):
        """
        指定した日数のVOLUMEを返します。
        :param pair: 通貨ペア
        :param global_end: 終了日
        :param days: 日数。終了日からこの日数を引いた分が開始日となる
        :param forward: シフト
        :return:
        """
        start = global_end - (DAY * days) - forward
        end = global_end - forward
        chart = self.get_chart_until_success(pair=pair, period=DAY, start=start, end=end)
        result = 0
        for one_day in chart:
            if pair.startswith("BTC_"):
                result += one_day['volume']
            else:
                result += one_day["quoteVolume"]
        return result

    def get_chart_until_success(self, pair, start, period, end):
        return get_chart_until_success(self._polo, pair, start, period, end)


coinList = CoinList()