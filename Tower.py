import sys
import pygame
import math
from Engine.AssetManager import load_image


def distance(obj1, obj2):
    try:
        return math.hypot(obj2[0] - obj1[0], obj2[1] - obj1[1])
    except TypeError:
        #enemy
        return math.hypot(obj2.x - obj1.x, obj2.y - obj1.y)

class BasicTower(object):
    def __init__(self, x, y, slot, game):
        self.game = game
        self.default_direction = None
        self.x = x
        self.y = y
        self.attack_range = 70
        self.damage = 10
        self.fire_rate = 1.0
        self.attacking = False
        self.target = None
        self.angle = 0
        self.image = load_image("tower.png")
        self.rotated_image = self.image
        self.image_rect = self.image.get_rect()
        self.last_image_update = 0
        self.last_image_update_max = 10
        self.set_default_direction(slot)

    def set_default_direction(self, slot):
        if slot.facing == "down":
            self.default_direction = 270
        elif slot.facing == "up":
            self.default_direction = 90
        elif slot.facing == "left":
            self.default_direction = 180
        elif slot.facing == "right":
            self.default_direction = 0
        self.angle = self.default_direction
        self.update_image_rotation()


    def draw(self, canvas):
        canvas.blit(self.rotated_image, (self.x, self.y))
        pygame.draw.circle(canvas, (255, 255, 255), (self.x + int((self.image_rect.width / 2)), self.y + int((self.image_rect.height / 2))), self.attack_range, 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image_rect.width, self.image_rect.height)

    def update(self, dt):
        #if we don't have a target, search for one
        if not self.target:
            self.set_target(self.scan_for_enemies())
        
        #do we have a target?
        if self.target:
            #if so, is it in range
            if not self.in_range(self.target):
                print("Target out of range, setting to none")
                self.target = None
        self.update_image(dt)
        

    def in_range(self, obj):
        dist = distance(self, obj)
        if dist > self.attack_range:
            return False
        return True

    def get_angle(self, origin, target):
        dx = target.x - origin.x
        dy = target.y - origin.y
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degs = math.degrees(rads)

        return int(degs)

    def update_image_rotation(self):
        old_center = self.image.get_rect().center
        rotated_image = self.rot_center(self.image, self.angle)
        self.rotated_image = rotated_image
        self.rotated_image.get_rect().center = old_center

    def update_image(self, dt):
        self.last_image_update += dt
        if self.last_image_update > self.last_image_update_max:
            self.last_image_update = 0
            if self.target:
                self.angle = self.get_angle(self, self.target)
                print("Angle: {}".format(self.angle))
                self.update_image_rotation()
            else:
                #we don't have a target, reset
                if self.angle > self.default_direction:
                    self.angle -= 1
                elif self.angle < self.default_direction:
                    self.angle += 1
                self.update_image_rotation()

    def handle_event(self, event):
        pass

    def set_target(self, target):
        print("Setting Target")
        self.target = target

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        print("Rotating image by angle: {}".format(angle))
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def scan_for_enemies(self):
        found = None
        closest = sys.maxsize
        for enemy in self.game.get_enemy_list():
            e_dist = distance(self.get_rect(), enemy.get_rect())
            if e_dist < closest and e_dist < self.attack_range:
                found = enemy
                closest = e_dist
        print("Found: {}".format(found))
        return found


class TowerSlot(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.surface = load_image("open_spot.png")

    def draw(self, canvas):
        r = self.surface.get_rect()
        
        canvas.blit(self.surface, (self.x, self.y))
        
    def get_rect(self):
        i = self.surface.get_rect()
        return pygame.Rect(self.x, self.y, i.width, i.height)

    def update(self, dt):
        pass

    def handle_event(self, event):
        pass