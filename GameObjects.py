from SpriteClass import Sprite
from time import clock as game_clock
from random import uniform, randint


class Meteor(Sprite):
    """ The class is used to create instances of meteors with different speeds and sizes"""

    def __init__(self, image_file, top, left):
        super().__init__(image_file, top, left)
        self.velocity_x = uniform(3.0, 6.0)
        self.velocity_y = uniform(2.0, 3.0)

    def update(self):
        """ Method controls tha passive movement of the meteor """
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


class Failure:
    """ The class is responsible for setting the possibility of failure in ship`s controls(creates an alert)"""

    def __init__(self):
        self.probability = randint(int(game_clock()) + 4, int(game_clock()) + 10)
        self.randomness = randint(1, 3)

    def reset_probability(self):
        self.probability = randint(int(game_clock()) + 5, int(game_clock()) + 10)
        self.randomness = randint(1, 3)

    def block_control(self):  # determines which controls will be disabled for the certain period of time
        if self.randomness == 1:
            return 1
        elif self.randomness == 2:
            return 2
        else:
            return 3


class StatusBar:
    """ This might be created using the 'Singleton' design pattern, because there is only one status bar in a game """

    def __init__(self, screen):
        self.score = 0
        self.screen = screen

    def draw_text(self, message, position, font, color=(170, 10, 10)):
        text = font.render(message, False, color)
        self.screen.blit(text, position)
