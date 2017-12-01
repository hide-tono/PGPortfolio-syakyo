import json
import time
from datetime import datetime

# 時間定数
from urllib.parse import urlencode
from urllib.request import urlopen, Request

minute = 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365

# 実行可能コマンド群
PUBLIC_COMMANDS = ['returnTicker', 'return24hVolume', 'returnOrderBook', 'returnTradeHistory', 'returnChartData', 'returnCurrencies', 'returnLoanOrders']


class Poloniex:
    def __init__(self, APIKey='', Secret=''):
        self.APIKey = APIKey.encode()
        self.Secret = Secret.encode()
        # ---変換関数---
        # timestampを%Y-%m-%d %H:%M:%Sフォーマットの文字列に変換
        self.timestamp_str = lambda timestamp=time.time(), date_format="%Y-%m-%d %H:%M:%S": datetime.fromtimestamp(timestamp).strftime(date_format)
        # %Y-%m-%d %H:%M:%Sフォーマットの文字列をUNIX時刻に変換
        self.str_timestamp = lambda date_str=self.timestamp_str(), date_format="%Y-%m-%d %H:%M:%S": int(time.mktime(time.strftime(date_str, date_format)))
        # 0～1を0%～100%に変換する
        self.float_roundPercent = lambda floatN, decimalP=2: str(round(float(floatN) * 100, decimalP)) + '%'
        # ----パブリックコマンド----
        # https://poloniex.com/support/api/
        '''
        Returns the ticker for all markets. Sample output:
        {"BTC_LTC":{"last":"0.0251","lowestAsk":"0.02589999","highestBid":"0.0251","percentChange":"0.02390438",
        "baseVolume":"6.16485315","quoteVolume":"245.82513926"},"BTC_NXT":{"last":"0.00005730","lowestAsk":"0.00005710",
        "highestBid":"0.00004903","percentChange":"0.16701570","baseVolume":"0.45347489","quoteVolume":"9094"}, ... }
        '''
        self.marketTicker = lambda x=0: self.api('returnTicker')
        '''
        Returns the 24-hour volume for all markets, plus totals for primary currencies. Sample output:
        {"BTC_LTC":{"BTC":"2.23248854","LTC":"87.10381314"},"BTC_NXT":{"BTC":"0.981616","NXT":"14145"}, ... 
        "totalBTC":"81.89657704","totalLTC":"78.52083806"}'''
        self.marketVolume = lambda x=0: self.api('return24hVolume')
        '''
        Returns information about currencies. Sample output:
        {"1CR":{"maxDailyWithdrawal":10000,"txFee":0.01,"minConf":3,"disabled":0},
        "ABY":{"maxDailyWithdrawal":10000000,"txFee":0.01,"minConf":8,"disabled":0}, ... }'''
        self.marketStatus = lambda x=0: self.api('returnCurrencies')
        '''
        Returns the list of loan offers and demands for a given currency, specified by the "currency" GET parameter. Sample output:
        {"offers":[{"rate":"0.00200000","amount":"64.66305732","rangeMin":2,"rangeMax":8}, ... ],
        "demands":[{"rate":"0.00170000","amount":"26.54848841","rangeMin":2,"rangeMax":2}, ... ]}'''
        self.marketLoans = lambda coin: self.api('returnLoanOrders', {'currency': coin})
        '''Returns the order book for a given market, as well as a sequence number for use with the Push API 
        and an indicator specifying whether the market is frozen. 
        You may set currencyPair to "all" to get the order books of all markets. Sample output:
        {"asks":[[0.00007600,1164],[0.00007620,1300], ... ], "bids":[[0.00006901,200],[0.00006900,408], ... ], 
        "isFrozen": 0, "seq": 18849}'''
        self.marketOrders = lambda pair='all', depth=10: self.api('returnOrderBook', {'currencyPair': pair, 'depth': depth})
        '''
        Returns candlestick chart data. Required GET parameters are "currencyPair", "period" (candlestick period in seconds; 
        valid values are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end". "Start" and "end" are 
        given in UNIX timestamp format and used to specify the date range for the data returned. Sample output:
        [{"date":1405699200,"high":0.0045388,"low":0.00403001,"open":0.00404545,"close":0.00427592,"volume":44.11655644,
        "quoteVolume":10259.29079097,"weightedAverage":0.00430015}, ...]'''
        self.marketChart = lambda pair, period=day, start=time.time() - (week * 1), end=time.time(): self.api('returnChartData', {'currencyPair': pair, 'period': period, 'start': start, 'end': end})
        # Poloniexがバグを修正する必要がある
        '''
        Returns your trade history for a given market, specified by the "currencyPair" POST parameter. 
        You may specify "all" as the currencyPair to receive your trade history for all markets. 
        You may optionally specify a range via "start" and/or "end" POST parameters, 
        given in UNIX timestamp format; if you do not specify a range, it will be limited to one day. 
        You may optionally limit the number of entries returned using the "limit" parameter, up to a maximum of 10,000. 
        If the "limit" parameter is not specified, no more than 500 entries will be returned. Sample output:
        [{ "globalTradeID": 25129732, "tradeID": "6325758", "date": "2016-04-05 08:08:40", 
        "rate": "0.02565498", "amount": "0.10000000", "total": "0.00256549", "fee": "0.00200000", "orderNumber": "34225313575", 
        "type": "sell", "category": "exchange" }, { "globalTradeID": 25129628, "tradeID": "6325741", 
        "date": "2016-04-05 08:07:55", "rate": "0.02565499", "amount": "0.10000000", "total": "0.00256549", 
        "fee": "0.00200000", "orderNumber": "34225195693", "type": "buy", "category": "exchange" }, ... ]'''
        self.marketTradeHist = lambda pair: self.api('returnTradeHistory', {'currencyPair': pair})

    def api(self, command, args=None):
        """
        APIを実行します。
        returns コマンドが不正であったりプライベートであった場合はFalseを返します。APIエラーの場合は{"error":"<error message>"}を返します。
        """
        if args is None:
            args = {}
        if command in PUBLIC_COMMANDS:
            url = 'https://poloniex.com/public?'
            args['command'] = command
            ret = urlopen(Request(url + urlencode(args)))
            return json.loads(ret.read().decode(encoding='UTF-8'))
        else:
            return False
