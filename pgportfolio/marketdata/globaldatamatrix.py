import sqlite3

from pgportfolio.marketdata.coinlist import CoinList
from pgportfolio.trade.constants import DATABASE_DIR, FIVE_MINUTES




class HistoryManager:
    """
    ヒストリカルデータをsqliteで管理するクラス。
    """

    def __init__(self, coin_number, end, volume_average_days=1, volume_forward=0, online=True):
        """
        :param coin_number:
        :param end:
        :param volume_average_days:
        :param volume_forward:
        :param online: Falseだとcoin_listがNoneになる
        """
        self.initialize_db()
        self.__storage_period = FIVE_MINUTES  # 300秒
        self._coin_number = coin_number
        self._online = online
        if self._online:
            self._coin_list = CoinList(end, volume_average_days, volume_forward)
        # FIXME

    def initialize_db(self):
        with sqlite3.connect(DATABASE_DIR) as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS History ('
                           'date INTEGER, '
                           'coin VARCHAR(20),'
                           'high FLOAT,'
                           'low FLOAT,'
                           'open FLOAT,'
                           'close FLOAT,'
                           'volume FLOAT,'
                           'quoteVolume FLOAT,'
                           'weightedAverage FLOAT,'
                           'PRIMARY KEY(date, coin)'
                           ');')
            connection.commit()
