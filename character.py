import pygame as pg
from resource_path import resource_path

class Character:
    def __init__(self, screen):
        self.screen = screen
        self.still_sheet = pg.image.load(resource_path("images/still.png"))
        self.walk_sheet = pg.image.load(resource_path("images/walking.png"))
        self.original_still_images = self.load_images(self.still_sheet, 16, 30)
        self.original_walk_images = self.load_images(self.walk_sheet, 16, 30)
        self.scale_factor = 1.0  # Default scale factor
        self.still_images = self.scale_images(self.original_still_images, self.scale_factor)
        self.walk_images = self.scale_images(self.original_walk_images, self.scale_factor)
        self.current_image = self.still_images[3]  # Start with the correct still frame
        self.rect = self.current_image.get_rect()
        self.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.speed = 5
        self.direction = 1  # Start with the correct direction
        self.is_walking = False

    def load_images(self, sheet, sprite_width, sprite_height):
        images = []
        cols = sheet.get_width() // sprite_width
        rows = sheet.get_height() // sprite_height
        for row in range(rows):
            for col in range(cols):
                image = pg.Surface((sprite_width, sprite_height), pg.SRCALPHA)
                image.blit(sheet, (0, 0), (col * sprite_width, row * sprite_height, sprite_width, sprite_height))
                images.append(image)
        return images

    def scale_images(self, images, scale):
        return [pg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))) for img in images]

    def set_still_image(self):
        if self.direction == 0:  # Up
            self.current_image = self.still_images[1]
        elif self.direction == 1:  # Down
            self.current_image = self.still_images[3]
        elif self.direction == 2:  # Left
            self.current_image = self.still_images[2]
        elif self.direction == 3:  # Right
            self.current_image = self.still_images[0]

    def update(self, direction, collision_detector=None):
        old_rect = self.rect.copy()
        self.is_walking = direction is not None

        if direction == 0:  # Up
            self.rect.y -= self.speed
            self.direction = 0
        elif direction == 1:  # Down
            self.rect.y += self.speed
            self.direction = 1
        elif direction == 2:  # Left
            self.rect.x -= self.speed
            self.direction = 2
        elif direction == 3:  # Right
            self.rect.x += self.speed
            self.direction = 3

        if collision_detector is not None and collision_detector.check_collision(self):
            self.rect = old_rect

        if not self.is_walking:
            self.set_still_image()


    def set_scale(self, scale_factor):
        self.scale_factor = scale_factor
        self.still_images = self.scale_images(self.original_still_images, scale_factor)
        self.walk_images = self.scale_images(self.original_walk_images, scale_factor)
        old_center = self.rect.center
        self.rect.size = self.still_images[0].get_size()
        self.rect.center = old_center
        self.speed = int(5 * scale_factor)  # Adjust speed based on scale

    
    def set_direction(self, direction):
        self.direction = direction
        self.is_walking = False
        self.set_still_image()

    def draw(self):
        if self.is_walking:
            if self.direction == 0:  # Up
                start_frame = 6
            elif self.direction == 1:  # Down
                start_frame = 18
            elif self.direction == 2:  # Left
                start_frame = 12
            elif self.direction == 3:  # Right
                start_frame = 0
            
            frame = (pg.time.get_ticks() // 100) % 4
            self.current_image = self.walk_images[start_frame + frame]
        else:
            self.set_still_image()
        
        self.screen.blit(self.current_image, self.rect)

# Test code
if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Character Sprite Test")
    clock = pg.time.Clock()

    character = Character(screen)
    character.set_scale(2.0)  # Start with a scale of 2.0

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_PLUS or event.key == pg.K_EQUALS:
                    character.set_scale(character.scale_factor + 0.1)
                elif event.key == pg.K_MINUS:
                    character.set_scale(max(0.1, character.scale_factor - 0.1))

        keys = pg.key.get_pressed()
        direction = None
        if keys[pg.K_UP]:
            direction = 0
        elif keys[pg.K_DOWN]:
            direction = 1
        elif keys[pg.K_LEFT]:
            direction = 2
        elif keys[pg.K_RIGHT]:
            direction = 3

        character.update(direction)

        screen.fill((255, 255, 255))  # Fill the screen with white
        character.draw()
        pg.display.flip()
        clock.tick(60)

pg.quit()