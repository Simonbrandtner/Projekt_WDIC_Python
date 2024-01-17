from random import randint, choice
from entity import Entity

class Enemy(Entity):
    """init an enemy"""
    def __init__(self, rect, surface, category, spawn_height_range=(200, 300)):
        Entity.__init__(self, rect)
        self.category = category
        self.surface = surface
        self.speed = (0,0)
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
    
    




   