import pygame
from settings import *
from random import randint

# Class that contains all the functions to play magic
class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/Fire.wav')
        }

    # Function for healing magic
    def heal(self, player, strength, cost, groups):
        # Healing player if the cost required (energy) > player's energy
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            # Making sure health stays as much as max allowed health
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    # Function for doing flames or burning magic
    def flame(self, player, cost, groups):
        # Same logic as healing magic
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()

            # PLaying the flame animations according to player's direction
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)

            # Adding a little offset to the animations
            for i in range(1,6):
                if direction.x: # Horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3 )
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3 )
                    self.animation_player.create_particles('flame', (x,y), groups)
                else: # Vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx  + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)