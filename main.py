from argparse import ArgumentParser
import os


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--mode', dest='mode', metavar='MODE', default='train',
                        help='start mode, train, generate, download_data, backtest')
    parser.add_argument('--processes', dest='processes', default='1',
                        help='number of processes you want to start to train the network')
    parser.add_argument('--repeat', dest='repeat', default='1',
                        help='repeat times of generating training subfolder')
    parser.add_argument('--algo', dest='algo',
                        help='algo name or indices of training_package')
    parser.add_argument('--algos', dest='algos',
                        help='algo names or indices of training_packag, separated by ","')
    parser.add_argument('--labels', dest='labels',
                        help='names that will shown in the figure caption or table header')
    parser.add_argument('--format', dest='format', default='raw',
                        help='format of the table printed')
    parser.add_argument('--device', dest='device', default='cpu',
                        help='device to be used to train')
    parser.add_argument('--folder', dest='folder', type=int,
                        help='folder(int) to load the config, neglect this option if loading from'
                             './pgportfolio/net_config')
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    if not os.path.exists('./train_package'):
        os.makedirs('./train_package')
    if not os.path.exists('./database'):
        os.makedirs('./database')

    if options.mode == 'train':
        import pgportfolio.autotrain.training


if __name__ == 'main':
    main()