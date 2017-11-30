import json
import logging
from os import path, os


def add_packages(config, repeat=1):
    """
    train_package以下に数字のサブディレクトリを作成します。
    :param config: コンフィグ
    :param repeat: 新規に作成するサブディレクトリの個数
    :return:
    """
    # train_packageの絶対パスを取得
    train_dir = 'train_package'
    package_dir = path.realpath(__file__).replace('pgportfolio/autotrain/generate.pyc', train_dir) \
        .replace("pgportfolio\\autotrain\\generate.pyc", train_dir) \
        .replace('pgportfolio/autotrain/generate.py', train_dir) \
        .replace("pgportfolio\\autotrain\\generate.py", train_dir)
    all_subdir = [int(s) for s in os.listdir(package_dir) if os.path.isdir(package_dir + '/' + s)]
    if all_subdir:
        max_dir_num = max(all_subdir)
    else:
        max_dir_num = 0
    indices = []

    # repeatの数だけサブディレクトリを作成する
    for i in range(repeat):
        max_dir_num += 1
        directory = package_dir + "/" + str(max_dir_num)
        config["random_seed"] = i
        os.makedirs(directory)
        indices.append(max_dir_num)
        with open(directory + "/" + "net_config.json", 'w') as outfile:
            json.dump(config, outfile, indent=4, sort_keys=True)
    logging.info("create indexes %s" % indices)
    return indices
