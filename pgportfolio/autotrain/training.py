import logging


def train_all(processes=1, device='cpu'):
    '''
    train_packageディレクトリ内のすべてのエージェントをトレーニングします。
    :param processes: プロセス数。
    :param device:
    '''
    if processes == 1:
        console_level = logging.INFO
        logging_level = logging.DEBUG

