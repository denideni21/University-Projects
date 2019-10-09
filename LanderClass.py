import pygame
from random import randint, uniform
from math import sin, cos, radians
from SpriteClass import Sprite
from LanderAttributes import FuelTank, EngineFire


class Lander(Sprite):
    """        Implementation of the LANDER Class         """

    def __init__(self, max_width, fuel_capacity=500):
        super().__init__('images/lander.png', 10, randint(0, 1123))  # call Sprite initializer
        self.width = max_width
        # This variable holds the rotated image if the lander is being rotated or the original image by default
        self.rotatedImg = self.image
        # This method takes the actual size of the image ignoring its transparent parts
        self.mask = pygame.mask.from_surface(self.rotatedImg)

        """Initializing lander's attributes: 
            the default angle, its lives, the current altitude after spawn, 
            the damage percentage and setting random velocities for the lander moving on x and y"""
        self.velocity_x = uniform(-1.0, 1.0)
        self.velocity_y = uniform(0.0, 1.0)
        self.rotation_angle = 0
        self.lives = 3
        self.altitude = 1000
        self.damage = 0

        # The fuel_tank tank of the ship is an instance of an other class(has-a relationship)
        self.fuel_tank = FuelTank(fuel_capacity)

    def fall_down(self):
        """ Method implements the effect of Mars'es gravitation on the lander """
        self.velocity_y += 0.03
        self.rect.left += self.velocity_x
        self.rect.bottom += self.velocity_y

        # check and control the behaviour of the lander according its position on the screen size
        if self.rect.right < 0:
            self.rect.left = self.width

        if self.rect.left > self.width:
            self.rect.right = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = uniform(0.0, 1.0)

    def rotate(self,  direction=None):  # rotates ship to the left or right by 1 degree
        if direction == "left":
            self.rotation_angle += 1 % 360
        elif direction == 'right':
            self.rotation_angle -= 1 % 360
        self.rotatedImg = pygame.transform.rotate(self.image, self.rotation_angle)

    def control_keys(self, key_pressed, alerted_key=None):  # handling keyboard inputs and alerts
        fire = None

        if alerted_key != key_pressed[pygame.K_RIGHT] and key_pressed[pygame.K_RIGHT]:
            self.rotate('right')

        if alerted_key != key_pressed[pygame.K_RIGHT] and key_pressed[pygame.K_SPACE]:
            fire = EngineFire(self.rect, self.rotation_angle)   # create thrust from lander`s engines
            self.activate_engines()

        if alerted_key != key_pressed[pygame.K_RIGHT] and key_pressed[pygame.K_LEFT]:
            self.rotate('left')

        return fire

    def activate_engines(self):
        """ This method is helps the ship to counter-react the gravitation effect of the planet """
        self.velocity_y -= 0.33 * cos(radians(self.rotation_angle))
        self.velocity_x += 0.33 * sin(radians(-self.rotation_angle))
        self.fuel_tank.consume_fuel()  # method implemented in class FuelTank

    def get_altitude(self):  # calculates the current altitude of the ship
        return 1000 - (self.rect.top * 1.436)

    def reset_stats(self):
        """ Method resets all the attributes of the lander to default """
        self.rect.left = randint(0, 1200 - self.rect.width)  # spawns the ship on a different place on the top
        self.rect.top = 0
        self.velocity_y = uniform(0.0, 1.0)
        self.velocity_x = uniform(-0.1, 1.0)
        self.rotatedImg = self.image
        self.rotation_angle = 0
        self.fuel_tank.reset_fuel_level()
        self.damage = 0

    def receive_damage(self, dmg):
        self.damage += dmg

    def check_landing_condition(self):
        ship_landing_condition = [True if self.fuel_tank.level() > 0 and self.damage < 100 else False]
        return ship_landing_condition[0] and (self.velocity_y < 5) and (-5 < self.velocity_x < 5
                                                                        ) and (-7 <= self.rotation_angle <= 7)
