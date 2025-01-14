import pygame as pg
from resource_path import resource_path

class IntroScene:
    def __init__(self, screen, character, dialogue_manager):
        self.screen = screen
        self.character = character
        self.dialogue_manager = dialogue_manager
        self.prof_oak_image1 = pg.image.load(resource_path("images/Professor Oak.png"))
        self.prof_oak_image1 = pg.transform.scale(self.prof_oak_image1, (self.prof_oak_image1.get_width()*4, self.prof_oak_image1.get_height()*4))
        self.prof_oak_image2 = pg.image.load(resource_path("images/leftprofoak.png"))
        self.prof_oak_image2 = pg.transform.scale(self.prof_oak_image2, (self.prof_oak_image2.get_width()*4, self.prof_oak_image2.get_height()*4))
        
        self.prof_oak_pos1 = (192, 180)
        self.prof_oak_pos2 = (192, 180)  # Adjust this position as needed
        self.image_bg = pg.image.load(resource_path("images/Professor Oak copy.png"))
        self.prof_oak_pos = (192,180)
        self.dialogue_step = 0
        self.character_moved = False
        self.dialogue_sound = pg.mixer.Sound(resource_path("sounds/Pokemon A Button Sound.ogg"))
        self.state = "WAITING"  # New initial state
        self.delay_timer = 0
        self.delay_duration = 4000  # 3 seconds delay (adjust as needed)
        self.animation_started = False
        self.animation_timer = 0
        self.animation_duration = 7000  # 4 seconds for the animation
        self.character_start_pos = (400, 500)
        self.character_mid_pos = (400, 210)
        self.character_end_pos = (300, 210)

        self.surprise_duration = 1500  # 1.5 seconds for the surprise animation
        self.surprise_directions = [3, 2, 3, 0]  # right, left, right, up
        self.surprise_index = 0
        self.character_scale = 3.4
        
        self.clock = pg.time.Clock()
        self.choice = None
        self.dialogue_position_set = False
        

    def update_animation(self):
        # Calculate direction_change_interval at the beginning of each update
        self.direction_change_interval = self.surprise_duration / len(self.surprise_directions)

        dt = self.clock.tick(60)
        self.animation_timer += dt

        total_duration = self.surprise_duration + self.animation_duration
        progress = min(self.animation_timer / total_duration, 1)
        
        if progress < self.surprise_duration / total_duration:
            # Surprise animation
            direction_index = int(self.animation_timer / self.direction_change_interval)
            if direction_index < len(self.surprise_directions):
                self.character.set_direction(self.surprise_directions[direction_index])
            new_x, new_y = self.character_start_pos
        elif progress < 0.75:
            # Move up
            move_progress = (progress - self.surprise_duration / total_duration) / (0.75 - self.surprise_duration / total_duration)
            new_x = self.character_start_pos[0]
            new_y = self.character_start_pos[1] + (self.character_mid_pos[1] - self.character_start_pos[1]) * move_progress
            self.character.set_direction(0)  # Set direction up
            self.character.is_walking = True
        else:
            # Move left
            move_progress = (progress - 0.75) / 0.25
            new_x = self.character_mid_pos[0] + (self.character_end_pos[0] - self.character_mid_pos[0]) * move_progress
            new_y = self.character_mid_pos[1]
            self.character.set_direction(2)  # Set direction left
            self.character.is_walking = True
        
        self.character.rect.center = (int(new_x), int(new_y))
        
        if progress >= 1:
            self.character.set_direction(2)  # Ensure character is facing left at the end
            self.state = "DIALOGUE"
            self.character.is_walking = False
            self.animation_started = False

    def update(self):
        if self.state == "WAITING":
            self.delay_timer += self.clock.tick(60)
            if self.delay_timer >= self.delay_duration:
                self.state = "ANIMATION"
                self.animation_timer = 0  # Reset animation timer
                self.character.is_walking = False  # Ensure character isn't walking during surprise
        elif self.state == "ANIMATION":
            self.update_animation()
        elif self.state == "DIALOGUE":
            return self.handle_dialogue()
        return None



    def handle_dialogue(self):
        if self.dialogue_step == 0:
            narrator_text = "Prof. Oak: Ehi, sveglia dormiglione!"
            question = "Hai mai pensato che la tua vita potrebbe essere un videogioco mal programmato?"
            choices = ["Uh, cosa?", "Ogni giorno, prof"]
            self.choice = self.dialogue_manager.draw_dialogue(narrator_text, question, choices)
            if self.choice:
                self.dialogue_step = 1
                self.dialogue_sound.play()
                return None
        elif self.dialogue_step == 1:
            if self.choice == "Uh, cosa?":
                narrator_text = "Prof. Oak: Ah, vedo che sei sveglio come un Snorlax dopo pranzo. Perfetto, sei il candidato ideale!"
            else:
                narrator_text = "Prof. Oak: Ottimo! Un po' di esistenzialismo adolescenziale è proprio quello che ci serve!"
            question = "Cosa ne pensi?"
            choices = ["Per cosa?", "Ho paura di chiedere"]
            choice = self.dialogue_manager.draw_dialogue(narrator_text, question, choices)
            if choice == "Per cosa?":
                self.choice = "Curioso"
            else:
                self.choice = "Scettico"
            self.dialogue_step = 2
            self.dialogue_sound.play()
            return None
        elif self.dialogue_step == 2:
            if self.choice == "Curioso":
                narrator_text = "Prof. Oak: Per un viaggio nel tempo, ovviamente!"
                question = "Cosa potrebbe mai andare storto?"
            else:
                narrator_text = "Prof. Oak: Troppo tardi per avere paura!"
                question = "Stai per diventare il mio... ehm, il nostro eroe!"
            choices = ["Suona pericoloso", "Fantastico!"]
            choice = self.dialogue_manager.draw_dialogue(narrator_text, question, choices)
            if choice == "Suona pericoloso":
                self.choice = "Cauto"
            else:
                self.choice = "Entusiasta"
            self.dialogue_step = 3
            self.dialogue_sound.play()
            return None
        elif self.dialogue_step == 3:
            if self.choice == "Cauto":
                narrator_text = "Prof. Oak: Pericoloso? Nah, al massimo potresti cancellare la tua stessa esistenza. Niente di che!"
            else:
                narrator_text = "Prof. Oak: Adoro il tuo entusiasmo! Spero che tu sia altrettanto entusiasta dei paradossi temporali!"
            question = "Sei pronto per questa avventura?"
            choices = ["Continua"]
            if self.dialogue_manager.draw_dialogue(narrator_text, question, choices) == "Continua":
                self.dialogue_sound.play()
                self.dialogue_step = 4
            return None
        elif self.dialogue_step == 4:
            narrator_text = "Prof. Oak: Bene, ora che sei completamente informato e consenziente (legalmente parlando), prepariamoci per questa avventura totalmente sicura e ben ponderata!"
            question = "Sei pronto a partire?"
            choices = ["Sono pronto!", "Aiuto..."]
            choice = self.dialogue_manager.draw_dialogue(narrator_text, question, choices)
            if choice:  
                self.dialogue_sound.play()
                return "DONE"
        return None


    def draw(self):
        self.image_bg_scaled = pg.transform.scale(self.image_bg, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(self.image_bg_scaled, (0, 0))
        
        if self.state == "WAITING" or self.state == "ANIMATION":
            self.screen.blit(self.prof_oak_image1, self.prof_oak_pos1)
        else:
            self.screen.blit(self.prof_oak_image2, self.prof_oak_pos2)
        
        if self.state != "WAITING":
            self.character.draw()
        
        if self.state == "DIALOGUE":
            self.dialogue_manager.draw()