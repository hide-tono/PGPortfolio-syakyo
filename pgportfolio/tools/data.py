def get_volume_forward(time_span, portion, portion_reserved):
    volume_forward = 0
    if not portion_reserved:
        volume_forward = time_span * portion
    return volume_forward


def get_chart_until_success(polo, pair, start, period, end):
    """
    成功するまでPoloniexからチャートデータを取得します
    :param polo: Poloniexクラス
    :param pair: 通貨ペア
    :param start: 開始時刻
    :param period: 時間足
    :param end: 終了時刻
    :return: チャートデータ
    """
    is_connect_success = False
    chart = {}
    while not is_connect_success:
        try:
            chart = polo.marketChart(pair=pair, start=int(start), period=int(period), end=int(end))
            is_connect_success = True
        except Exception as e:
            print(e)
    return chart
