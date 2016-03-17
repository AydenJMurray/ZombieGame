__author__ = 'leif'
from faker import Factory as FakeFactory
from house import House
import math
import random

class Street(object):

    def __init__(self, name, house_list):
        self.name = name
        self.num_of_houses = len(house_list)
        self.current_house = 0
        self.house_list = house_list

    def get_current_house(self):
        return self.house_list[self.current_house]

    def move_to_next_house(self):
        if self.current_house < (self.num_of_houses-1):
            self.current_house += 1
            return True
        return False

    def move_to_house(self,i):
        if (i >= 0) and (i < self.num_of_houses):
            self.current_house = i
            return True
        return False

    def anymore_house(self):
        if self.current_house < self.num_of_houses:
            return True
        return False

    def __str__(self):
        return 'Street Name: {0} Number of Houses: {1} at house no. {2}'.format(self.name, self.num_of_houses, self.current_house)


class StreetFactory(object):

    def __init__(self):
        self.faker = FakeFactory.create()

    def make_street(self, player_state):

        # how many houses in street?

        number_of_houses = random.randint(5,8)

        # name of street
        street_name = '{0} {1}'.format(self.faker.street_name(), self.faker.street_suffix())
        house_list = []
        for i in range(0, number_of_houses):
            a_house = House(player_state)
            house_list.append(a_house)

        street = Street(street_name, house_list)

        return street