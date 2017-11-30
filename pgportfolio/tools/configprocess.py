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
    else:
        with open(rootpath+"/pgportfolio/" + "net_config.json") as file:
            config = json.load(file)
    return preprocess_config(config)


def preprocess_config(config):
    """
    デフォルト値を入れます
    """
    fill_default(config)
    # 以下は3系なのでいらない


def fill_default(config):
    """
    コンフィグにデフォルト値を入れます。
    :param config:
    """
    set_missing(config, 'random_seed', 0)
    set_missing(config, 'agent_type', 'NNAgent')
    fill_layers_default(config['layers'])
    fill_input_default(config["input"])
    fill_train_config(config["training"])


def set_missing(config, name, value):
    """
    キーがない場合に値をセットします
    """
    if name not in config:
        config[name] = value


def fill_layers_default(layers):
    """
    レイヤーのデフォルト値をセットします
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


def fill_input_default(input_config):
    """
    入力に関するデフォルト値をセットします
    """
    set_missing(input_config, "save_memory_mode", False)
    set_missing(input_config, "portion_reversed", False)
    set_missing(input_config, "market", "poloniex")
    set_missing(input_config, "norm_method", "absolute")
    set_missing(input_config, "is_permed", False)
    set_missing(input_config, "fake_ratio", 1)


def fill_train_config(train_config):
    """
    トレーニングに関するデフォルト値をセットします
    """
    set_missing(train_config, "fast_train", True)
    set_missing(train_config, "decay_rate", 1.0)
    set_missing(train_config, "decay_steps", 50000)
