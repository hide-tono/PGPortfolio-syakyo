import logging

import os
import time

from multiprocessing import Process

from pgportfolio.learn.tradertrainer import TraderTrainer
from pgportfolio.tools.configprocess import load_config


def train_one(save_path, config, log_file_dir, index, logfile_level, console_level, device):
    """
    エージェントをトレーニングします。
    :param save_path: TensorFlowのモデル(.ckpt)を保存するパス。None可。
    :param config: jsonのコンフィグファイル
    :param log_file_dir: TensorBoardのログファイルを保存するディレクトリ。None可。
    :param index: トレーニングを一意に定めるインデックス。train_packageのサブディレクトリ名。
    :param logfile_level: ファイルのログレベル
    :param console_level: コンソールのログレベル
    :param device: 0ならCPU、1ならGPU。
    :return: 結果のnamedtuple
    """
    if log_file_dir:
        logging.basicConfig(filename=log_file_dir.replace('tensorboard', 'programlog'),
                            lovel=logfile_level)
        console = logging.StreamHandler()
        console.setLevel(console_level)
        logging.getLogger().addHandler(console)
    print('training at %s started' % index)
    trainer = TraderTrainer(config, save_path=save_path, device=device)
    return trainer.train_net(log_file_dir=log_file_dir, index=index)


def train_all(processes=1, device='cpu'):
    """
    train_packageディレクトリ内のすべてのエージェントをトレーニングします。
    :param processes: プロセス数。ログレベルにも影響します。
    :param device: CPUとGPUのどちらを使用するか
    """
    if processes == 1:
        console_level = logging.INFO
        logfile_level = logging.DEBUG
    else:
        console_level = logging.WARNING
        logfile_level = logging.INFO
    train_dir = 'train_package'
    if not os.path.exists('./' + train_dir):
        os.makedirs('./' + train_dir)
    all_subdir = os.listdir('./' + train_dir)
    all_subdir.sort()
    # プロセスプール。train_package以下で未実行の数字ディレクトリを実効する
    pool = []
    for subdir in all_subdir:
        if not str.isdigit(subdir):
            # 数字ディレクトリ以外は許容しない
            return
        if not (os.path.isdir('./' + train_dir + '/' + subdir + '/tensorboard') or
                    os.path.isdir('./' + train_dir + '/' + subdir + '/logifle')):
            # 未実行の数字ディレクトリのみ実行する
            p = Process(target=train_one,
                        # train_oneの引数
                        args=("./" + train_dir + "/" + subdir + "/netfile",
                              load_config(subdir),
                              "./" + train_dir + "/" + subdir + "/tensorboard",
                              subdir, logfile_level, console_level, device))
            p.start()
            pool.append(p)
        else:
            continue
            
        # プロセスが多すぎる場合を考慮
        wait = True
        while wait:
            time.sleep(5)
            for p in pool:
                alive = p.is_alive()
                if not alive:
                    pool.remove(p)
            if len(pool) < processes:
                wait = False
    print('全タスクが終了しました。')
