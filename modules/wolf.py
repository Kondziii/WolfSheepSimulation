import logging
import math


class Wolf(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.last_victim_index = None
        logging.debug('Wolf(' + str(self.x) + ',' + str(self.y) + ') was called, constructor')
        logging.info('Wolf initial position at ' + '[' + str(self.x) + ', ' + str(self.y) + ']')

    def __lookForVictim(self, sheeps):

        """Method that returns a distance from the
        nearest sheep and her index."""

        victim_index = 0
        min_distance = float('inf')
        for index, sheep in enumerate(sheeps):
            if sheep.alive:
                distance = (math.dist(sheep.getCoordinates(), self.getCoordinates()))
                if distance < min_distance:
                    min_distance = distance
                    victim_index = index
        logging.debug('Wolf.__lookForVictim(' + str(sheeps) + ') was called, returns '
                      + str(min_distance) + str(victim_index))
        return min_distance, victim_index

    def move(self, wolf_move_dist, sheeps):

        """Method for checking whether the nearest sheep is
        within the range of a wolf. According to the outcome
        of this check it changes the coordinates of the wolf."""

        log_info = 'Wolf moved: [' + str(self.x) + ', ' + str(self.y) + ']'
        min_distance, victim_index = self.__lookForVictim(sheeps)

        if wolf_move_dist >= min_distance:
            self.x, self.y = sheeps[victim_index].getCoordinates()
            sheeps[victim_index].getHunted()
            self.last_victim_index = victim_index
            logging.info("Wolf hunted sheep number " + str(victim_index)
                         + '(counting from 0)' + ' at distance ' + str(min_distance))
        else:
            self.x += wolf_move_dist * ((sheeps[victim_index].x - self.x) / min_distance)
            self.y += wolf_move_dist * ((sheeps[victim_index].y - self.y) / min_distance)
            self.last_victim_index = None
        log_info += '---->> [' + str(self.x) + ', ' + str(self.y) + ']'
        logging.debug('Wolf.move(' + str(wolf_move_dist) + ',' + str(sheeps) + ') was called')
        logging.info(log_info)

    def getCoordinates(self):

        """Method returns the current coordinates of
        the object as vector."""

        logging.debug('Wolf.getCoordinates() was called, returns ' + str(self.x) + str(self.y))
        return [self.x, self.y]
