import json
import os

# Windows対応？
import sys

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


def preprocess_config(config):
    fill_default(config)
    if sys.version_info[0] == 2:
        return byteify(config)
    else:
        return config


def fill_default(config):
    """
    コンフィグにデフォルト値を入れます。
    :param config:
    """
    set_missing(config, 'random_seed', 0)
    set_missing(config, 'agent_type', 'NNAgent')
    fill_layers_default(config['layers'])


def set_missing(config, name, value):
    """
    キーがない場合に値を詰めます
    """
    if name not in config:
        config[name] = value


def fill_layers_default(layers):
    """
    レイヤーのデフォルト値を詰めます
    :param layers:
    """
    for layer in layers:
        if layer["type"] == "ConvLayer":
            set_missing(layer, "padding", "valid")
            set_missing(layer, "strides", [1, 1])
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "EIIE_Dense":
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "DenseLayer":
            set_missing(layer, "activation_function", "relu")
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "EIIE_LSTM" or layer["type"] == "EIIE_RNN":
            set_missing(layer, "dropouts", None)
        elif layer["type"] == "EIIE_Output" or \
                        layer["type"] == "Output_WithW":
            set_missing(layer, "regularizer", None)
            set_missing(layer, "weight_decay", 0.0)
        elif layer["type"] == "DropOut":
            pass
        else:
            raise ValueError("layer name {} not supported".format(layer["type"]))
