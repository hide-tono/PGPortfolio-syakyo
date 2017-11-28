import logging

import os
import time

from multiprocessing import Process


def train_one(args):
    pass


def load_config(dir):
    pass


def train_all(processes=1, device='cpu'):
    '''
    train_packageディレクトリ内のすべてのエージェントをトレーニングします。
    :param processes: プロセス数。ログレベルにも影響します。
    :param device: CPUとGPUのどちらを使用するか
    '''
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
    all.subdir.sort()
    # プロセスプール。train_package以下で未実行の数字ディレクトリを実効する
    pool = []
    for dir in all_subdir:
        if not str.isdigit(dir):
            # 数字ディレクトリ以外は許容しない
            return
        if not (os.path.isdir('./' + train_dir + '/' + dir + '/tensorboard') or
                    os.path.isdir('./' + train_dir + '/' + dir + '/logifle')):
            # 未実行の数字ディレクトリのみ実行する
            p = Process(target=train_one,
                        # train_oneの引数
                        args=("./" + train_dir + "/" + dir + "/netfile",
                              load_config(dir),
                              "./" + train_dir + "/" + dir + "/tensorboard",
                              dir, logfile_level, console_level, device))
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
