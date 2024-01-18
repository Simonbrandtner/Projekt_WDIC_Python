import pygame
from random import randint, choice
from entity import Entity

class Projectile(Entity):
    def __init__(self, rect, color, radius, speed):
        Entity.__init__(self, rect)
        self.color = color
        self.radius = radius
        self.speed = speed

    def move(self):
        """Bewegt das Projektil."""
        self.position = (self.position[0] + self.speed[0], self.position[1] + self.speed[1])
        self.rect.center = self.position

    def display(self, screen):
        """Zeichnet das Projektil als Kreis."""
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def enemy_restriction(self):
        # Beispiel: Überprüft, ob das
        #  Projektil links außerhalb des Bildschirms ist
        screen_width=300
        screen_height=100
        if self.position[0] < 0 or self.position[0] > screen_width:  # screen_width muss definiert sein
            return True
        if self.position[1] < 0 or self.position[1] > screen_height:  # screen_height muss definiert sein
            return True
        return False  

class Enemy(Entity):
    """init an enemy"""
    def __init__(self, rect, surface, category, spawn_height_range=(200, 300)):
        Entity.__init__(self, rect)
        self.category = category
        self.surface = surface
        self.speed = (0,0)
        self.last_shot_time = 0  # Initialisieren Sie last_shot_time hier


        # Setzt die Startposition der fliegenden Gegner in einem zufälligen Bereich.
        if self.category in ["flyingMob", "flyingMob2"]:
            self.set_random_vertical_position(spawn_height_range)
        else:
            self.position = self.rect.topleft

    def set_random_vertical_position(self, height_range):
        """Setzt die vertikale Position des fliegenden Gegners in einem zufälligen Bereich."""
        x, _ = self.rect.topleft
        y = randint(*height_range)
        self.position = (x, y)
        self.rect.topleft = self.position

    def enemy_restriction(self):
        """return true if enemy left his rect restriction"""
        height,_ = self.position
        width = self.rect.size[1]
        if self.category == "grass":
            if height + width < 0:
                return True
        else:
            if height + width < 0:
                return True
        return False

    def display(self, screen):
        """displaying the enemy"""
        screen.blit(self.surface, self.rect)

    def moving(self):
        """verif if moving"""
        return self.speed != (0,0)

    def run(self, speed):
        """animate the mob with random vertical movement"""
        vertical_movement_range = (-50, 50)  # Beispielbereich für vertikale Bewegung

        if self.category in ["flyingMob", "flyingMob2", "ScaryMob"]:
            # Zufällige vertikale Geschwindigkeit für fliegende Gegner
            vertical_speed = choice(vertical_movement_range)
            self.change_speed((speed, vertical_speed))
        elif self.category == "heart":
            self.change_speed((speed + randint(0, 500), 0))
        elif self.category == "mediumMob":
            self.change_speed((speed + speed * 0.05, 0))
        else:
            self.change_speed((speed, 0))

    def shoot(self, color, radius, projectile_speed, spawn_offset=(0,0)):
        """Lässt den Gegner ein Projektil schießen."""
        projectile_rect = self.rect.copy()  # Erstellt eine Kopie des Rechtecks des Gegners
        projectile_rect.center = (self.position[0] + spawn_offset[0], self.position[1] + spawn_offset[1])
        return Projectile(projectile_rect, color, radius, projectile_speed)
