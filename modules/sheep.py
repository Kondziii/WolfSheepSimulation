import logging
import random


class Sheep(object):
    def __init__(self, init_pos_limit):
        self.init_pos_limit = init_pos_limit
        self.x, self.y = [random.uniform(-self.init_pos_limit, self.init_pos_limit) for x in range(2)]
        self.alive = True
        logging.debug('Sheep (' + str(init_pos_limit) + ') was called, constructor')
        logging.info('Sheep initial position at ' + '[' + str(self.x) + ', ' + str(self.y) + ']')

    def move(self, sheep_move_dist):

        """ Method that enable to rand direction according to the rule
        up - 0, right - 1, down - 2, left - 3a and then move."""
        direction = None
        log_info = 'Sheep moved: [' + str(self.x) + ', ' + str(self.y) + ']'

        if self.alive:
            direction = random.randint(0, 3)
            if direction == 0:
                self.y += sheep_move_dist
            elif direction == 1:
                self.x += sheep_move_dist
            elif direction == 2:
                self.y -= sheep_move_dist
            else:
                self.x -= sheep_move_dist
        log_info += '---->> [' + str(self.x) + ', ' + str(self.y) + '] direction: ' + str(direction)

        logging.debug('Sheep.move(' + str(sheep_move_dist) + ') was called')
        logging.info(log_info)

    def getCoordinates(self):

        """Method returns the current coordinates of
        the object as vector."""

        logging.debug('Sheep.getCoordinates() was called, returns ' + str(self.x) + str(self.y))
        return [self.x, self.y]

    def getHunted(self):

        """Method that should be invoked only when
        the object has been hunted, it sets properly
        the attributes of hunted sheep."""

        logging.debug('Sheep.getHunted() was called')
        self.alive = False
        self.x, self.y = None, None
