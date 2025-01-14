import pygame as pg

class CollisionDetector:
    def __init__(self, background):
        self.background = background
        
    def check_collision(self, character):
        for rect in self.background.collision_rects:
            if character.rect.colliderect(rect):
                return True
        return False