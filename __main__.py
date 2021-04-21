import argparse
import configparser
import logging

from chase.modules.simulation import Simulation


def main():
    round_number = 50
    sheeps_number = 15
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    directory = None
    wait = None

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        action='store', help='set config file',
                        metavar='FILE', dest='config_file')

    parser.add_argument('-d', '--dir', action='store', type=str,
                        help="choose directory where files will be saved",
                        metavar='DIR', dest='directory')

    parser.add_argument('-l', '--log', action='store',
                        help="create log file", metavar='LEVEL',
                        dest='log_level')

    parser.add_argument('-r', '--rounds', action='store',
                        help='choose the number of rounds',
                        metavar='NUM', dest='rounds_number_parser')

    parser.add_argument('-s', '--sheep', action='store', help="choose the number of sheeos",
                        metavar='NUM', dest='sheeps_number_parser')

    parser.add_argument('-w', '--wait', help='wait after every round until key is pressed, yes or no - default no',
                        dest='wait')
    args = parser.parse_args()

    if args.config_file:
        conf_parser = configparser.ConfigParser()
        conf_parser.read(args.config_file)
        init_pos_limit = float(conf_parser.get('Terrain', 'InitPosLimit'))
        sheep_move_dist = float(conf_parser.get('Movement', 'SheepMoveDist'))
        wolf_move_dist = float(conf_parser.get('Movement', 'WolfMoveDist'))

    if init_pos_limit <= 0 or sheep_move_dist <= 0 or wolf_move_dist <= 0:
        logging.error("Entered distance properties should be positive numbers")
        raise ValueError("Entered distance properties should be positive numbers")

    if args.directory:
        directory = str(args.directory)

    if args.log_level:
        if args.log_level == "DEBUG" or args.log_level == '10':
            level = logging.DEBUG
        elif args.log_level == "INFO" or args.log_level == '20':
            level = logging.INFO
        elif args.log_level == "WARNING" or args.log_level == '30':
            level = logging.WARNING
        elif args.log_level == "ERROR" or args.log_level == '40':
            level = logging.ERROR
        elif args.log_level == "CRITICAL" or args.log_level == '50':
            level = logging.CRITICAL
        else:
            logging.error("The entered log level is incorrect")
            raise ValueError("The entered log level is incorrect")
        logging.basicConfig(filename='chase.log', filemode='w', level=level)

    if args.rounds_number_parser:
        round_number = int(args.rounds_number_parser)

    if args.sheeps_number_parser:
        sheeps_number = int(args.sheeps_number_parser)

    if round_number <= 0 or sheeps_number <= 0:
        logging.error("Incorrect value of rounds number or sheeps number")
        raise ValueError("Incorrect value of rounds number or sheeps number")

    if args.wait:
        if args.wait == 'yes' or args.wait == 'YES' or args.wait == 'y' or args.wait == 'Y' or args.wait == 'Yes':
            wait = str(args.wait)
        elif args.wait == 'no' or args.wait == 'NO' or args.wait == 'n' or args.wait == 'N' or args.wait == 'No':
            wait = None
        else:
            logging.warning("Unknown value of wait option")

    Simulation().conductSimulation(
        round_number, sheeps_number
        , init_pos_limit, sheep_move_dist
        , wolf_move_dist, directory, wait)


if __name__ == '__main__':
    main()
