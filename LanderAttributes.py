import pygame
from SpriteClass import Sprite


class EngineFire(Sprite):
    """ Sprite created to initialize the thrust of the lander when the engines are activated """

    def __init__(self, lander_rect, lander_rotation_angle):
            super().__init__('images/thrust.png', lander_rect.bottom - 10, lander_rect.left + 31)
            self.rotatedImg = pygame.transform.rotate(self.image, lander_rotation_angle)


class FuelTank:
    """ This class implements the fuel tank tank of the spaceship """

    def __init__(self, quantity):
        self.quantity = quantity
        self.fuel_lvl = quantity

    def level(self):  # returns the current fuel_tank level
        return self.quantity

    def consume_fuel(self):  # burns fuel_tank every time the engines are started
        self.quantity -= 5

    def reset_fuel_level(self):  # resets the fuel_tank level back to default
        self.quantity = self.fuel_lvl

    def set_fuel_lvl(self, amount=0):  # enables the user to set a new value to the fuel_tank level
        self.quantity = amount
