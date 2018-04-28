import os
import random

class Pymagotchi:

    def __init__(self, name, hunger=10, strength=10):
        self._name = name 
        self._hunger, self._HUNGER_MAX = hunger, hunger
        self._strength, self._STRENGTH_MAX = strength, strength
        self._age = 0
        self._time = 0
        self._state = 'pymagotchi'
        self._eating = 0


    def get_state(self):
        return self._state


    def events(self):
        if self._state != 'dead':    
            self._time += 1
            if self._time % 10 == 0:
                self._age += 1
            if self._age == 5:
                self._state = 'dead'

            if self._eating != 0:
                self._eating -= 1
            else:
                self._state = 'pymagotchi'

            if self._hunger != 0 and self._eating == 0:
                self._hunger -= 1
            if self._hunger == 0:
                if self._strength != 0:
                    self._strength -= 1
            if self._strength == 0:
                self._state = 'dead'

            if self._hunger < 8 and self._eating == 0:
                food = os.listdir('food')
                if food:
                    to_eat = random.choice(food)
                    print(f'{self._name} mange {to_eat}')
                    os.remove(f'food/{to_eat}')
                    self._hunger = self._HUNGER_MAX
                    self._strength = self._STRENGTH_MAX
                    self._state = 'eat'
                    self._eating = 3


    def get(self, attribute):
        if attribute == 'FAIM':
            return f'{self._hunger:2}'
        if attribute == 'FORCE':
            return f'{self._strength:2}'
        if attribute == 'NOM':
            return f'{self._name}'
        if attribute == 'AGE':
            return f'{self._age:2}'
