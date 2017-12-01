from pgportfolio.tools.data import get_volume_forward
import pgportfolio.marketdata.globaldatamatrix as gdm

class DataMatrices:
    def __init__(self, start, end, period, batch_size=50, volume_average_days=30, buffer_bias_ratio=0,
                 market='poloniex', coin_filter=1, window_size=50, feature_number=3, test_portion=0.15,
                 portion_reserved=False, online=False, is_permed=False):
        """
        :param start: 開始時間（UNIX時間）
        :param end: 終了時間（UNIX時間）
        :param period:入力行列にアクセスできる期間
        :param batch_size:バッチサイズ
        :param volume_average_days:
        :param buffer_bias_ratio:
        :param market:
        :param coin_filter: 使用するコインの数
        :param window_size:入力データの数
        :param feature_number:特徴量の数。1～4 (2は未実装)
        :param test_portion:開始時間・終了時間の間で使用する割合(0～1)?
        :param portion_reserved:部分でtestとtrainのどちらを使用するか。
        Falseだとtrain, validation, test, Trueだとtest, validation, train。Boolean
        :param online:
        :param is_permed:
        """
        start = int(start)
        self.__end = int(end)

        # window_sizeがMIN_NUM_PERIOD以上であること
        self.__coin_no = coin_filter
        type_list = get_type_list(feature_number)
        self.__features = type_list
        self.feature_number = feature_number
        volume_forward = get_volume_forward(self.__end - start, test_portion, portion_reserved)
        self.__history_manager = gdm.HistoryManager(coin_number=coin_filter, end=self.__end,
                                                    volume_average_days=volume_average_days,
                                                    volume_forward=volume_forward, online=online)
        # FIXME


def get_type_list(feature_number):
    """
    特徴量名のリストを返します。
    :param feature_number: 特徴量の数。1～4 (2は未実装)
    :return: 1:close, 2:close, volume, 3:close, high, low, 4:close, high, low, open
    """
    if feature_number == 1:
        return ['close']
    elif feature_number == 2:
        raise NotImplementedError("volumeは未実装")
    elif feature_number == 3:
        return ['close', 'high', 'low']
    elif feature_number == 4:
        return ['close', 'high', 'low', open]
    else:
        raise ValueError('feature_numberは1-4で指定してください')
