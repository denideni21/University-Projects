import pygame
from random import randint
from SpriteClass import Sprite
from LanderClass import Lander
from GameObjects import Meteor, StatusBar, Failure
from time import clock as game_clock


class Game:
    """Initializing game`s default settings."""
    def __init__(self, frames=30, width=1200, height=750):
        self.FPS = frames
        self.screen_width = width
        self.screen_height = height
        self.game = True
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.clock = pygame.time.Clock()
        self.caption = pygame.display.set_caption("Mars Lander v01.9")

        """ Creating the objects we will need to start the game """
        #####################################################################################################
        self.background = Sprite('images/mars_background_instr.png', 0, 0)

        # Status bar:
        self.status_bar = StatusBar(self.screen)

        # Instance of the mars lander
        self.mars_lander = Lander(width, fuel_capacity=500)

        # Landing pads - adding them to a group, as they have the same behaviour:
        self.landing_pads = pygame.sprite.Group()
        Sprite('images/pad.png', randint(690, 725), randint(80, 242)).add(self.landing_pads)
        Sprite('images/pad_tall.png', randint(630, 670), randint(400, 642)).add(self.landing_pads)
        Sprite('images/pad_tall.png', 655, randint(800, 1042)).add(self.landing_pads)

        # Obstacles - adding them to a group, as they have the same behaviour:
        self.obstacles = pygame.sprite.Group()
        Sprite("images/building_dome_small.png", 580, 220).add(self.obstacles)
        Sprite("images/rocks_NW_small.png", 525, 440).add(self.obstacles)
        Sprite("images/satellite_SW_small.png", 450, 1130).add(self.obstacles)
        Sprite("images/satellite_SE_small.png", 650, 30).add(self.obstacles)
        Sprite("images/pipe_stand_SE_small.png", 525, 50).add(self.obstacles)

        # Meteors - adding them to a group, as they have the same behaviour:
        self.meteors = pygame.sprite.Group()
        for i in range(randint(5, 10)):  # randomly choosing the number of the meteors
            image_name = 'images/spaceMeteors_00{}.png'.format(randint(1, 4))  # choose a random image for each meteor
            Meteor(image_name, randint(0, 100), randint(0, 150)).add(self.meteors)  # create instances

        self.controls_failure = Failure()  # Initialize an alert possibility

        # Fonts:
        self.font_arial_black = pygame.font.SysFont('Arial Black', 18)
        self.font_verdana = pygame.font.SysFont('Verdana', 35)
        self.font_arial_black_large = pygame.font.SysFont('Arial Black', 50)
        self.font_verily_mono = pygame.font.SysFont('Verily Serif Mono', 27)

        self.meteor_storm = False  # Changes to True if there was a storm already in the current round
        self.storm_probability = randint(int(game_clock()) + 7, int(game_clock()) + 14)  # Choose random time for storm
        #####################################################################################################

    def reset_storm_probability(self):
        clock_now = int(game_clock())
        self.storm_probability = randint(clock_now + 3, clock_now + 12)

    def game_loop(self):
        """ That is the main game loop which controls the event flow """

        while self.game:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # if the user clicks on the [X] button the loop stops
                    self.game = False

            #######################################################################
            """ Displaying the images and stats on the screen"""
            self.screen.blit(self.background.image, self.background.rect)

            self.landing_pads.draw(self.screen)
            self.obstacles.draw(self.screen)

            """ Display the stats on the screen """
            self.status_bar.draw_text("LIVES: {}".format(self.mars_lander.lives), (155, 80), self.font_verily_mono)
            self.status_bar.draw_text("{:.2f} s".format(game_clock()), (75, 12), self.font_verily_mono)
            self.status_bar.draw_text("{:.2f} m/s".format(self.mars_lander.velocity_x), (280, 35),
                                      self.font_verily_mono)
            self.status_bar.draw_text("{:.2f} m/s".format(self.mars_lander.velocity_y), (280, 55),
                                      self.font_verily_mono)
            self.status_bar.draw_text("{} kg".format(self.mars_lander.fuel_tank.level()), (75, 35),
                                      self.font_verily_mono)
            self.status_bar.draw_text("{:.0f} m".format(self.mars_lander.get_altitude()), (280, 12),
                                      self.font_verily_mono)
            self.status_bar.draw_text(str(self.status_bar.score), (75, 85), self.font_verily_mono, color=(255, 255, 26))
            self.status_bar.draw_text("{} %".format(self.mars_lander.damage), (100, 55), self.font_verily_mono)
            ########################################################################

            #########################################
            """ Checking for collision b/w the lander and any of the obstacles"""
            obstacles_hit = pygame.sprite.spritecollide(self.mars_lander, self.obstacles, True)
            # destroy obstacle after collision with lander and deal 10 damage
            self.mars_lander.receive_damage(10 * len(obstacles_hit))
            #########################################

            if self.mars_lander.lives == 0:  # the game stops if the lander has no more lives
                self.game = False

            if not self.meteor_storm and game_clock() > self.storm_probability:
                # a random meteor storm is spawned if there hasn't been one in the current round already
                self.meteor_storm = True

            if self.meteor_storm:  # the storm is active if there are still meteors flying around
                self.meteors.update()   # controls tha passive movement of the meteors
                self.meteors.draw(self.screen)

                meteors_hit = pygame.sprite.spritecollide(self.mars_lander, self.meteors, True)
                # if there is a collision, destroy meteor and deal 25 damage to the ship
                self.mars_lander.receive_damage(25 * len(meteors_hit))

            keys_pressed = pygame.key.get_pressed()    # get all keys pressed while playing

            if keys_pressed[pygame.K_ESCAPE]:
                self.game = False  # terminate the game loop

            if self.mars_lander.fuel_tank.level() <= 0:     # if lander runs out of fuel(0), disable all controls
                self.mars_lander.fuel_tank.set_fuel_lvl(0)
                msg = self.font_arial_black_large.render("You Ran Out Of Fuel...Falling!", False, (255, 0, 6))
                self.screen.blit(msg, (200, 320))
                self.screen.blit(self.mars_lander.rotatedImg, self.mars_lander.rect)

            elif self.mars_lander.damage >= 100:    # if lander is too damaged(100%), disable all controls
                self.mars_lander.damage = 100
                msg = self.font_verdana.render("The ship is too damaged..disabling controls!!!", False, (199, 0, 150))
                self.screen.blit(msg, (210, 320))
                self.screen.blit(self.mars_lander.rotatedImg, self.mars_lander.rect)

            else:  # if there is fuel and the ship is not damaged enough to fall
                if not self.controls_failure.probability < game_clock() < self.controls_failure.probability + 2:
                    # if there is not a failure in the lander`s controls(no alert case)
                    engine_thrust = self.mars_lander.control_keys(keys_pressed)
                    if engine_thrust:
                        self.screen.blit(engine_thrust.rotatedImg, engine_thrust.rect)
                        self.screen.blit(self.mars_lander.rotatedImg, self.mars_lander.rect)
                else:   # if there is an alert
                    msg = self.font_arial_black.render("*ALERT*", False, (0, 0, 255))
                    self.screen.blit(msg, (240, 90))
                    # disable a certain key according to the random number chosen by method block_control()
                    if self.controls_failure.block_control() == 1:
                        failed_key = keys_pressed[pygame.K_RIGHT]
                        self.mars_lander.control_keys(keys_pressed, failed_key)
                    elif self.controls_failure.block_control() == 2:
                        failed_key = keys_pressed[pygame.K_SPACE]
                        self.mars_lander.control_keys(keys_pressed, failed_key)
                    else:
                        failed_key = keys_pressed[pygame.K_LEFT]
                        self.mars_lander.control_keys(keys_pressed, failed_key)

                self.screen.blit(self.mars_lander.rotatedImg, self.mars_lander.rect)

            self.mars_lander.fall_down()    # passive movement of lander (gravity effect)
            pygame.display.update()

            landing_attempt = pygame.sprite.spritecollideany(self.mars_lander, self.landing_pads)
            # variable's value is equal to the landing pad instance colliding with the mars lander
            if landing_attempt or self.mars_lander.rect.bottom > self.screen_height:
                # check if lander either hit the bottom of the screen or one of the landing pads
                # reset objects, alert and storm for the next round
                self.create_new_meteors()
                self.reset_storm_probability()
                self.controls_failure.reset_probability()   # set new possibility of failure in the ship's controls
                self.reset_obstacles()
                self.meteor_storm = False

                if landing_attempt and self.mars_lander.rect.right < landing_attempt.rect.right and self.mars_lander.\
                        rect.left > landing_attempt.rect.left and self.mars_lander.check_landing_condition():
                    # if lander collides with a pad being fully between its borders, there is enough fuel and the damage
                    # is below 100%, the velocities are not exceeding the limit and the rotation angle is b/w -7 and 7
                    self.status_bar.score += 50
                    paused = self.pause_game('landed')  # returns true if user wants to quit the game
                    if paused:
                        return  # quits the loop
                else:
                    # if any of the above is false
                    self.mars_lander.lives -= 1
                    paused = self.pause_game('crashed')  # returns true if user wants to quit the game
                    if paused:
                        return  # quits the loop
                self.mars_lander.reset_stats()  # reset all attributes of the lander back to defaults

    def create_new_meteors(self):
        # deletes all old instances and populates tha group again
        self.meteors.empty()
        for m in range(randint(5, 10)):
            image = 'images/spaceMeteors_00{}.png'.format(randint(1, 4))
            Meteor(image, randint(0, 100), randint(0, 150)).add(self.meteors)

    def reset_obstacles(self):
        # recreates obstacles
        self.obstacles.empty()
        Sprite("images/building_dome_small.png", 580, 220).add(self.obstacles)
        Sprite("images/rocks_NW_small.png", 525, 440).add(self.obstacles)
        Sprite("images/satellite_SW_small.png", 450, 1130).add(self.obstacles)
        Sprite("images/satellite_SE_small.png", 650, 30).add(self.obstacles)
        Sprite("images/pipe_stand_SE_small.png", 525, 50).add(self.obstacles)

    def pause_game(self, msg_type):
        """ The method pauses the game after the player crashes and displays a message, till a key is pressed """
        msg = ''

        if msg_type == 'landed':
            msg = self.font_arial_black_large.render("Successful Landing!", False, (13, 109, 24))
        elif msg_type == 'crashed':
            msg = self.font_arial_black_large.render("You Have Crashed!", False, (255, 0, 6))

        self.screen.blit(msg, (330, 375))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Checks if the user wants to quit tha game by clicking on the "X" button
                    return True
                if event.type == pygame.KEYDOWN:
                    # Checks if any key is pressed - Resumes the game
                    return False

            pygame.display.update()
            self.clock.tick(self.FPS)
