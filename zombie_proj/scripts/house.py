__author__ = 'leif'
import random

class House(object):

    def __init__(self, player_state):
        self.room_list = []
        self.num_of_rooms = 0
        self.current_room = 0
        self.create_rooms(player_state)

    def get_house_stats(self):
        np = 0
        nf = 0
        na = 0
        nz = 0
        for room in self.room_list:
            np += room.people
            nf += room.food
            na += room.ammo
            nz += room.zombies

        return (np, nf, na, nz)


    def __str__(self):

        (np, nf, na, nz) = self.get_house_stats()
        return 'Number of Rooms: {0}: People: {1} Food: {2} Ammo: {3} Zombies: {4}'.format( self.num_of_rooms, np,nf,na,nz)



    def get_current_room(self):
        return self.room_list[self.current_room]

    def move_to_next_room(self):
        if self.current_room < self.num_of_rooms:
            self.current_room += 1
            return True
        return False

    def move_to_room(self, i):
        if (i >= 0) and (i < self.num_of_rooms):
            self.current_room = i
            return True
        return False

    def anymore_rooms(self):
        if self.current_room < self.num_of_rooms:
            return True
        return False


    def create_rooms(self, player_state):
        number_of_rooms = random.randint(7,13)

        for i in range(0, number_of_rooms):

            people = self.gen_people(player_state)
            food = self.gen_food(player_state, i)
            ammo = self.gen_ammo(player_state)
            zombies = self.gen_zombie(player_state, i)
            room = Room(people,food,ammo,zombies)

            self.room_list.append(room)
        self.num_of_rooms = number_of_rooms
        self.current_room = 0


    def gen_people(self, player_state):
        people = 0
        p = random.uniform(0,1)

        p_people = 0.2
        if player_state.party < 5:
            p_people += 0.05

        if p < p_people:
            people = random.randint(0,3)

        return people


    def gen_food(self, player_state, i):
        food = 0
        p = random.uniform(0,1)
        p_food = 0.71 - min(player_state.days*0.01,0.2)

        if p < p_food:
            f = random.randint(4,10)
            if f-i>0:
                food = f-i
            else:
                food = 0
        return food


    def gen_zombie(self,player_state,i):
        zombie = 0
        p = random.uniform(0,1)

        p_zombie = 0.1 + min(player_state.days * 0.005, 0.14) + (i*0.03)

        if p <p_zombie:
            zombie = random.randint(0,5)

        return zombie

    def gen_ammo(self,player_state):
        ammo = 0
        p = random.uniform(0,1)

        p_ammo = 0.22 + min(player_state.days * 0.005, 0.1)
        if p < p_ammo:
            if p < 0.05:
                ammo = random.randint(10,20)
            else:
                ammo = random.randint(1,4)
        return ammo


class Room(object):

    def __init__(self, people, food, ammo, zombies):
        self.people = people
        self.food = food
        self.ammo = ammo
        self.zombies = zombies
        self.visited = False


    def cleared(self):
        self.people = 0
        self.food = 0
        self.ammo = 0
        self.zombies = 0
        self.visited = True

    def __str__(self):
        return 'Room contains People: {people} Food: {food} Ammo: {ammo} Zombies: {zombies} Visted: {visited}'.format(**self.__dict__)