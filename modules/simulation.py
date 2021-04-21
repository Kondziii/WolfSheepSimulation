import csv
import json
import logging
import os

from chase.modules.sheep import Sheep
from chase.modules.wolf import Wolf


class Simulation(object):

    def __init__(self):
        self.sheeps = []
        self.wolf = None
        logging.debug('Simulation() was called, constructor')

    def __displayRoundInfo(self, round_number, victim_index, live_sheeps_number):

        """Method that is used for displaying
         current info after round."""

        print("Round number: ", round_number)
        print("Wolf position:", "[", round(self.wolf.x, 3), ",", round(self.wolf.y, 3), "]")
        print("Number of alive sheeps:", live_sheeps_number)
        if victim_index is not None:
            print("Sheep number", victim_index + 1, "has been hunted")
        print("-------------------------------------------------")
        logging.debug('Simulation.__displayRoundInfo(' + str(round_number) + ','
                      + str(victim_index) + ',' + str(live_sheeps_number) + ') was called')

    def __writeToJsonFile(self, round_number):

        """Method that is used for writing current round number,
        coordinates of the wolf and sheeps to pos.json file."""

        data = {'round_no': round_number, 'wolf_pos': [self.wolf.getCoordinates()], 'sheep_pos': []}
        for sheep in self.sheeps:
            data['sheep_pos'].append(sheep.getCoordinates())
        if round_number == 0:
            with open('pos.json', 'w') as file:
                json.dump(data, file, indent=4)
                file.write('\n')
        else:
            with open('pos.json', 'a') as file:
                json.dump(data, file, indent=4)
                file.write('\n')
        logging.debug('Simulation.__writeToJsonFile(' + str(round_number) + ') was called')

    def __writeToCsvFile(self, round_number, alive_sheeps_number):

        """Method designed for writing current round number and
        number of alive sheeps to alive.csv file."""

        fieldsname = ('round', 'sheeps alive')
        if round_number == 0:
            with open("alive.csv", 'w', newline='') as file_csv:
                csvwriter = csv.DictWriter(file_csv, fieldsname)
                csvwriter.writeheader()
                csvwriter.writerow({'round': round_number, 'sheeps alive': alive_sheeps_number})
        else:
            with open("alive.csv", 'a', newline='') as file_csv:
                csvwriter = csv.DictWriter(file_csv, fieldsname)
                csvwriter.writerow({'round': round_number, 'sheeps alive': alive_sheeps_number})
        logging.debug('Simulation.__writeToCsvFile(' + str(round_number) + ','
                      + str(alive_sheeps_number) + ') was called')

    def __changeDirectory(self, directory):

        """Method that changes working directory"""

        if not os.path.exists(os.path.join(os.getcwd(), directory)):
            logging.info("Directory " + str(os.path.join(os.getcwd(), directory))
                         + ' does not exists, it will be created')
            os.mkdir(directory)
        os.chdir(directory)
        logging.debug('Simulation.__changeDirectory(' + str(directory) + ') was called')

    def conductSimulation(self, rounds_number, sheeps_number, init_pos_limit, sheep_move_dist, wolf_move_dist,
                          directory, wait):

        """Method that starts simulation, it initializes wolf and sheep objects
        and then invokes their move method and it writes outcomes to the files."""

        self.wolf = Wolf()
        for i in range(sheeps_number):
            self.sheeps.append(Sheep(init_pos_limit))

        alive_sheeps_number = sheeps_number

        if directory:
            self.__changeDirectory(directory)

        self.__displayRoundInfo(0, self.wolf.last_victim_index, alive_sheeps_number)
        self.__writeToJsonFile(0)
        self.__writeToCsvFile(0, alive_sheeps_number)

        logging.info("Simulation is about to start")
        for round in range(rounds_number):
            for sheep in self.sheeps:
                sheep.move(sheep_move_dist)

            self.wolf.move(wolf_move_dist, self.sheeps)

            if self.wolf.last_victim_index is not None:
                alive_sheeps_number -= 1

            self.__displayRoundInfo(round + 1, self.wolf.last_victim_index, alive_sheeps_number)
            self.__writeToJsonFile(round + 1)
            self.__writeToCsvFile(round + 1, alive_sheeps_number)

            if alive_sheeps_number == 0:
                logging.info('Simulation ended before executing establishe number of rounds '
                             'due to the fact that there are not any alive sheeps')
                break

            if wait:
                input("Press any key to simulate next round ...")
            logging.info('Round number ' + str(round + 1) + ', Wolf position ['
                         + str(self.wolf.x) + ", " + str(self.wolf.y) + ']'
                         + ', Number of alive sheeps ' + str(alive_sheeps_number)
                         + ', Sheep that died in this round ' + str(self.wolf.last_victim_index))
        logging.info('The end of the simulation')
