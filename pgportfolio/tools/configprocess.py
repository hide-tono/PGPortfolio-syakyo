import json
import os

# Windows対応？
rootpath = os.path.dirname(os.path.abspath(__file__)). \
    replace('\\pgportfolio\\tools', '').replace('/pgportfolio/tools', '')


def load_config(index=None):
    """
    コンフィグをロードします
    :param index: train_package以下の数値。Noneならpgportfolioのデフォルト
    :return: コンフィグ
    """
    if index:
        with open(rootpath + '/train_package/' + str(index) + '/net_config.json') as file:
            config = json.load(file)
