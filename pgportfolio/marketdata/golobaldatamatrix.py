import sqlite3

from pgportfolio.trade.constants import DATABASE_DIR


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
        :param online: Falseだとcoin_listがNoneになる場合がある
        """
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(DATABASE_DIR) as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS History ('
                           'date INTEGER, '
                           'coin varchar(20),'
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

