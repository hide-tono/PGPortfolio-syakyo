import collections

Result = collections.namedtuple('Result',
                                ['Test_pv',
                                 'test_log_mean',
                                 'test_log_mean_free',
                                 'test_history',
                                 'config',
                                 'net_dir',
                                 'backtest_test_pv',
                                 'backtest_test_history',
                                 'backtest_test_log_mean',
                                 'training_time'])

class TraderTrainer:
    def __init__(self, config, fake_data=False, restore_dir=None, save_path=None, device='gpu', agent=None):
        """
        init
        :param config:
        :param fake_data:
        :param restore_dir:
        :param save_path:
        :param device:
        :param agent:
        """