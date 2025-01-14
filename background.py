import pygame as pg
import random
from resource_path import resource_path

class OptimizedBackground:
    def __init__(self, screen):
        self.screen = screen
        self.star_colors = [(255, 255, 255), (200, 200, 200), (150, 150, 150)]
        self.stars = self.generate_stars(100)
        self.star_speed = 0.5

        # Lazy load images
        self.images = {}
        self.scaled_images = {}

        # Collision rectangles
        self.collision_rects = [
            pg.Rect(0, 0, 10, screen.get_height()),
            pg.Rect(screen.get_width() - 10, 0, 10, screen.get_height()),
            pg.Rect(0, 0, screen.get_width(), 10),
            pg.Rect(0, screen.get_height() - 10, screen.get_width(), 10)
        ]
        self.group_rects = {
            "peppie": pg.Rect(0, 0, 200, 180)
        }

        # Initialize font for GAME OVER text
        self.font = None
    
    def load_image(self, image_path):
        """Lazy load an image."""
        if image_path not in self.images:
            self.images[image_path] = pg.image.load(resource_path(image_path)).convert_alpha()
        return self.images[image_path]

    def load_and_scale(self, image_path, size):
        """Load an image and scale it to the given size, with caching."""
        key = (image_path, size)
        if key not in self.scaled_images:
            image = self.load_image(image_path)
            self.scaled_images[key] = pg.transform.scale(image, size)
        return self.scaled_images[key]

    def generate_stars(self, num_stars):
        width, height = self.screen.get_size()
        return [
            (random.randint(0, width), random.randint(0, height), random.randint(1, 3), random.choice(self.star_colors))
            for _ in range(num_stars)
        ]

    def update(self):
        width, height = self.screen.get_size()
        self.stars = [
            (x, (y + self.star_speed) % height, size, color)
            for x, y, size, color in self.stars
        ]

    def draw(self, state):
        method_name = f"draw_{state.lower()}"
        draw_method = getattr(self, method_name, self.draw_default)
        draw_method()

    def draw_start_screen(self):
        self.draw_stars()

    def draw_introduction(self):
        self.draw_school_scene()

    def draw_peppie_dialogue(self):
        self.draw_school_scene()

    def draw_high_school_choice(self):
        self.draw_school_scene()

    def draw_move_to_peppie(self):
        self.draw_school_scene()

    def draw_america_choice(self):
        self.draw_school_scene()

    def draw_move_to_peppie_sardinia(self):
        self.draw_sardinia_scene()

    def draw_peppie_dialogue_sardinia(self):
        self.draw_sardinia_scene()

    def draw_sardinia_choice(self):
        self.draw_sardinia_scene()

    def draw_university_choice(self):
        self.screen.blit(self.load_and_scale("images/Pokemon FireRed Cerulean City.png", self.screen.get_size()), (0, 0))

    def draw_rome_scene(self):
        self.screen.blit(self.load_and_scale("images/rome.png", self.screen.get_size()), (0, 0))

    def draw_game_over(self):
        self.screen.fill((255, 0, 0))
        if self.font is None:
            self.font = pg.font.Font(None, 74)
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(game_over_text, text_rect)

    def draw_default(self):
        self.screen.fill((0, 0, 0))

    def draw_stars(self):
        self.screen.fill((0, 0, 0))
        for x, y, size, color in self.stars:
            pg.draw.rect(self.screen, color, (x, y, size, size))

    def draw_school_scene(self):
        self.screen.blit(self.load_and_scale("images/school.png", self.screen.get_size()), (0, 0))
        self.screen.blit(self.load_and_scale("images/letta.png", (58, 80)), (80, 100))
        self.screen.blit(self.load_and_scale("images/betta.png", (58, 80)), (10, 110))
        self.screen.blit(self.load_and_scale("images/keisi.png", (58, 80)), (50, 159))
        self.screen.blit(self.load_and_scale("images/lalla.png", (59, 95)), (150, 90))
        self.screen.blit(self.load_and_scale("images/ludo.png", (59, 95)), (120, 149))

    def draw_sardinia_scene(self):
        self.screen.blit(self.load_and_scale("images/Pokemon FireRed Four Island.png", self.screen.get_size()), (0, 0))
        self.screen.blit(self.load_and_scale("images/letta.png", (24.36, 33.6)), (100, 309))
        self.screen.blit(self.load_and_scale("images/keisi.png", (24.36, 33.6)), (84, 359))
        self.screen.blit(self.load_and_scale("images/lalla.png", (24.78, 39.9)), (84, 325))
        self.screen.blit(self.load_and_scale("images/ludo.png", (24.78, 39.9)), (110, 325))
        self.screen.blit(self.load_and_scale("images/betta.png", (24.36, 33.6)), (117, 359))

# The main() function remains unchanged