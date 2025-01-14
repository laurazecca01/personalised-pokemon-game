import pygame as pg
from background import OptimizedBackground
from dialogue import DialogueManager
from character import Character
from collision import CollisionDetector
from intro_scene import IntroScene
from resource_path import resource_path
import random

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.background = OptimizedBackground(screen)
        self.star_background = OptimizedBackground(screen)
        self.dialogue_manager = DialogueManager(screen, self)
        self.character = Character(screen)
        self.collision_detector = CollisionDetector(self.background)
        self.intro_scene = IntroScene(screen, self.character, self.dialogue_manager)
        self.start_screen_image = pg.image.load(resource_path("images/IMG_6178.PNG"))
        self.start_screen_image = pg.transform.scale(self.start_screen_image, (200, 270))
        self.peppie_rect = pg.Rect(0, 0, 350, 300) 
        self.peppie_rect_sardinia = pg.Rect(69, 300, 81, 97)
        self.win_font = pg.font.Font(resource_path("fonts/pokemon-ds-font.ttf"), 48)
        self.game_over_reason = None
        self.previous_state = None
        self.previous_choice = None
        self.clock = pg.time.Clock()
        self.fps = 60
        self.game_over_drawn = False
        self.finale_drawn = False
        self.character_positioned = False
        self.narrator = random.choice(["Paola", "Keisi", "Laura", "Betta"])
        self.dialogue_triggered = False
        self.conversation_available = False
        self.current_stage = "START_SCREEN"
        self.intro_scene_completed = False
        self.choice_made = False
        self.game_over_handled = False
        self.returning_from_game_over = False
        self.running = True

        self.choice_history = []
        self.can_start_peppie_dialogue_sardinia = False
        self.narrator = random.choice(["Paola", "Keisi", "Laura", "Betta"])


        self.bg_sounds = {
            'START_SCREEN': pg.mixer.Sound(resource_path('sounds/Pokemon Adventure.ogg')),
            'INTRO_SCENE': pg.mixer.Sound(resource_path('sounds/Professor Elms Lab.ogg')),
            "MAIN": pg.mixer.Sound(resource_path("sounds/Oreburgh City Day.ogg")),
            "SARDINIA": pg.mixer.Sound(resource_path("sounds/Twinleaf Town Night.ogg")),
            "ROME": pg.mixer.Sound(resource_path('sounds/Floaroma Town Day.ogg')),
            "GAME_OVER": pg.mixer.Sound(resource_path("sounds/Team Rocket Theme.ogg")),
            "VICTORY": pg.mixer.Sound(resource_path('sounds/Pokémon Frontier Brain Victory.ogg')),
            "CHOICES": pg.mixer.Sound(resource_path('sounds/Amity Square.ogg')),
        }

        pg.mixer.set_num_channels(8)
        self.bg_channel = pg.mixer.Channel(7)
        self.play_bg_sound("START_SCREEN")
        self.start_screen_delay = 30
        self.start_screen_counter = 0
        self.key_pressed = False
        self.intro_scene_done = False
        self.character_scale = 3.4
        self.character_scale_tiny = 1.5
    
    
    def reset_to_start_screen(self):
        self.change_state("START_SCREEN")
        self.dialogue_manager.reset()
        self.character.reset()
        self.intro_scene_completed = False
        self.choice_made = False
        self.returning_from_game_over = False
        self.game_over_reason = None
        self.play_bg_sound("START_SCREEN")
        self.running = True

    def change_state(self, new_state):
        print(f"Changing state from {self.current_stage} to {new_state}")
        self.current_stage = new_state
        self.dialogue_manager.current_stage = new_state
        self.choice_made = False
        self.update_background()

        if new_state == "GAME_OVER":
            self.play_bg_sound("GAME_OVER")
        elif new_state in ["MOVE_TO_PEPPIE"]:
            self.play_bg_sound("MAIN")
            self.character_positioned = False
            self.dialogue_manager.reset_dialogue()
            self.position_character()
            self.character.set_scale(self.character_scale)
            self.character.set_direction(1)  
            self.character.is_walking = False
        elif new_state in ["PEPPIE_DIALOGUE"]:
            self.play_bg_sound("MAIN")
        elif new_state in ["HIGH_SCHOOL_CHOICE", "AMERICA_CHOICE"]:
            self.play_bg_sound("CHOICES")
            self.character_positioned = False
            self.dialogue_manager.reset_dialogue()
            self.character.set_scale(self.character_scale)
            self.character.set_direction(1)  
            self.character.is_walking = False 
        elif new_state == "MOVE_TO_PEPPIE_SARDINIA":
            self.character_positioned = False
            self.character.set_scale(self.character_scale_tiny)
            self.position_character(289,300)
            self.play_bg_sound("SARDINIA")
            self.dialogue_manager.reset_dialogue()
        elif new_state == "PEPPIE_DIALOGUE_SARDINIA":
            self.play_bg_sound("SARDINIA")
        elif new_state == "SARDINIA_CHOICE":
            self.character_positioned = False
            self.play_bg_sound("SARDINIA")
            self.position_character(289,300)
            self.character.set_scale(self.character_scale_tiny)
            self.dialogue_manager.reset_dialogue()
        elif new_state == "UNIVERSITY_CHOICE":
            self.character_positioned = False
            self.play_bg_sound('ROME')
            self.character.set_direction(1) 
            self.character.set_scale(self.character_scale)
            self.position_character(130,258)
            self.character.is_walking = False
        elif new_state == "ROME_SCENE":
            self.character_positioned = False
            self.play_bg_sound('ROME')
            self.character.set_direction(1) 
            self.character.set_scale(self.character_scale)
            self.position_character(x=627,y=180)
            self.character.is_walking = False
        elif new_state == "FINALE_POSITIVO":
            self.position_character()
            self.play_bg_sound("VICTORY")
        elif new_state == "START_SCREEN":
            self.play_bg_sound("START_SCREEN")
        elif new_state == "INTRO_SCENE":
            self.play_bg_sound("INTRO_SCENE")
        elif new_state == "INTRODUCTION":
            self.character.set_scale(self.character_scale)
            self.position_character()
            self.play_bg_sound("MAIN")
        
    def position_character(self, x=None, y=None):
        if not self.character_positioned:
            self.character.set_scale(self.character_scale)
            
            if x is None and y is None:
                # Position at center if no coordinates are provided
                x = self.screen.get_width() // 2
                y = self.screen.get_height() // 2
            elif x is None:
                # If only y is provided, center horizontally
                x = self.screen.get_width() // 2
            elif y is None:
                # If only x is provided, center vertically
                y = self.screen.get_height() // 2
            
            self.character.rect.center = (x, y)
            self.character_positioned = True
            self.character.update(1)


    def update(self):
        self.background.update()
        
        stage_handlers = {
            "START_SCREEN": self.handle_start_screen,
            "INTRO_SCENE": self.handle_intro_scene,
            "MOVE_TO_PEPPIE": self.handle_move_to_peppie,
            "PEPPIE_DIALOGUE": self.handle_peppie_dialogue,
            "HIGH_SCHOOL_CHOICE": self.handle_high_school_choice,
            "AMERICA_CHOICE": self.handle_america_choice,
            "MOVE_TO_PEPPIE_SARDINIA": self.handle_move_to_peppie_sardinia,
            "PEPPIE_DIALOGUE_SARDINIA": self.handle_ppd_2,
            "SARDINIA_CHOICE": self.handle_sardinia_choice,
            "UNIVERSITY_CHOICE": self.handle_university_choice,
            "ROME_SCENE": self.handle_rome_scene,
            "GAME_OVER": self.handle_game_over,
            "FINALE_POSITIVO": self.handle_finale_positivo
        }
        
        if self.current_stage in stage_handlers:
            result = stage_handlers[self.current_stage]()
            if result == "QUIT" or result is False:
                self.running = False
        
        return self.running

    def update_background(self):
        self.background.update()
        self.background.draw(self.current_stage)
        pg.display.flip()
    
    def handle_start_screen(self):
        if self.dialogue_manager.draw_start_screen():
            self.change_state("INTRO_SCENE")

    def handle_intro_scene(self):
        if not self.intro_scene_completed:
            result = self.intro_scene.update()
            self.character.set_scale(self.character_scale)
            if result == "DONE":
                self.intro_scene_completed = True
                self.change_state("MOVE_TO_PEPPIE")

    def handle_move_to_peppie(self):
        self.character.set_scale(self.character_scale)
        self.position_character()
        self.update_character_movement()
        if self.character.rect.colliderect(self.peppie_rect):
            self.can_start_peppie_dialogue = True
            self.dialogue_manager.set_conversation_available("peppie")
        else:
            self.can_start_peppie_dialogue = False
            self.dialogue_manager.set_conversation_available(None)
    

    def handle_peppie_dialogue(self):
        # Ensure the character stays in the same direction during dialogue
        if not hasattr(self, 'dialogue_started'):
            self.dialogue_started = True
         

        result = self.dialogue_manager.handle_peppie_dialogue()
        if result in ["HIGH_SCHOOL_CHOICE", None]:
            self.change_state("HIGH_SCHOOL_CHOICE")
            self.dialogue_manager.reset_dialogue()
            self.dialogue_started = False
        elif result == "CONTINUE_DIALOGUE":
            pass  # Continue the dialogue

        return result


    def handle_move_to_peppie_sardinia(self):
        self.character.set_scale(self.character_scale_tiny)
        self.position_character()
        self.update_character_movement()

        # Check if the character is close to the Peppie group in Sardinia
        if self.character.rect.colliderect(self.peppie_rect_sardinia.inflate(50, 50)):  # Inflate to create a larger detection area
            self.can_start_peppie_dialogue_sardinia = True
            self.dialogue_manager.set_conversation_available("peppie")
        else:
            self.can_start_peppie_dialogue_sardinia = False
            self.dialogue_manager.set_conversation_available(None)
    

    def handle_ppd_2(self):
        result = self.dialogue_manager.handle_ppd_2()
        if result == "SARDINIA_CHOICE":
            self.change_state("SARDINIA_CHOICE")
            self.dialogue_manager.reset_dialogue()  # Reset dialogue state
        elif result == "CONTINUE_DIALOGUE":
            pass  # Continue the dialogue
        elif result is None:
            self.change_state("SARDINIA_CHOICE")
            self.dialogue_manager.reset_dialogue()
    
    def handle_high_school_choice(self):
        if not self.choice_made or self.returning_from_game_over:
            narrator_text = f"{self.narrator}: Davanti a te si presenta una scelta importante. Con chi vuoi passare i tuoi anni del liceo?"
            choices = ["Peppie", "Fighettini"]
            result = self.dialogue_manager.set_dialogue(narrator_text, "Scegli con saggezza:", choices)
            self.choice_made = True
            self.returning_from_game_over = False
            self.handle_choice_result("HIGH_SCHOOL_CHOICE", result)

    def handle_america_choice(self):
        if not self.choice_made or self.returning_from_game_over:
            narrator_text = f"{self.narrator}: Perfetto, hai scelto le persone giuste! Ma davanti a te si presenta un'altra scelta..."
            choices = ["Restare a Savona", "Andare in America"]
            result = self.dialogue_manager.set_dialogue(narrator_text, "Vuoi restare a Savona o andare a inseguire il tuo sogno americano?", choices)
            self.choice_made = True
            self.returning_from_game_over = False
            self.handle_choice_result("AMERICA_CHOICE", result)

    def handle_sardinia_choice(self):
        if not self.choice_made or self.returning_from_game_over:
            narrator_text = f"{self.narrator}: Accetti o meno i 5 euro di Laura per la pizza?"
            choices = ["Prima strillo un po'", "Sì, senza problemi"]
            result = self.dialogue_manager.set_dialogue(narrator_text, "Cosa fai?", choices)
            self.choice_made = True
            self.returning_from_game_over = False
            self.handle_choice_result("SARDINIA_CHOICE", result)

    def handle_university_choice(self):
        if not self.choice_made or self.returning_from_game_over:
            narrator_text = f"{self.narrator}: Sei proprio Lorenzo, questa storia verrà raccontata ai tuoi discendenti. Però ora davanti a te si presenta una scelta importante..."
            choices = ["Legge", "Architettura"]
            result = self.dialogue_manager.set_dialogue(narrator_text, "Cosa vuoi studiare all'università?", choices)
            self.choice_made = True
            self.returning_from_game_over = False
            self.handle_choice_result("UNIVERSITY_CHOICE", result)

    def handle_rome_scene(self):
        if not self.choice_made or self.returning_from_game_over:
            narrator_text = f"{self.narrator}: Vai a Roma, conosci persone molto simpatiche (non più di noi, ma veramente chi vorrebbe essere come noi). Studi legge senza problemi, prendi voti eccellenti, fino al momento in cui l'ansia inizia a farsi sentire..."
            choices = ["Scopri il \n poker online", "Ti impegni \n con costanza"]
            result = self.dialogue_manager.set_dialogue(narrator_text, "Come affronti questo momento difficile?", choices)
            self.choice_made = True
            self.returning_from_game_over = False
            self.handle_choice_result("ROME_SCENE", result)

    def split_and_display_text(self, text, question, choices):
        chunks = []
        current_chunk = ""
        sentences = text.split(". ")

        for i, sentence in enumerate(sentences):
            if i < len(sentences) - 1:
                sentence += "."  # Add the period back, except for the last sentence
            
            if len(current_chunk) + len(sentence) > 220:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
                else:
                    # If a single sentence is longer than 220 characters, we have to split it
                    chunks.append(sentence.strip())
            else:
                current_chunk += sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        for i, chunk in enumerate(chunks):
            if i < len(chunks) - 1:
                # For all chunks except the last one, we don't show choices
                result = self.dialogue_manager.draw_dialogue(chunk, None, ["Continua"])
                if result == "QUIT" or self.check_for_exit():  # Check for exit condition
                    return "QUIT"
            else:
                # For the last chunk, we show the question and choices
                result = self.dialogue_manager.draw_dialogue(chunk, question, choices)
                if result == "QUIT" or self.check_for_exit():  # Check for exit condition
                    return "QUIT"
                return result

        return None
   
    def handle_finale_positivo(self):
        if not self.choice_made:
            self.star_background.update()  # Update star animation
            self.star_background.draw_stars()  # Draw animated stars

            # Draw "YOU WON" text
            win_text = self.win_font.render("YOU WON", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(win_text, win_rect)

            # Draw character in the middle
            self.character.set_scale(self.character_scale)
            self.character.set_direction(1)  # Face forward
            self.character.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            self.character.draw()

            narrator_text = f"Narratore: Ti laurei, con tutti i tuoi cari, degli amici che ti vogliono forse fin troppo bene e che tu ricambi distruggendoli a paintball."
            choices = ["Ricomincia", "Esci dal gioco"]
            result = self.dialogue_manager.draw_dialogue(narrator_text, "E adesso cosa vuoi fare?", choices)
            
            if result:
                self.choice_made = True
                self.handle_choice_result("FINALE_POSITIVO", result)
 

    def handle_game_over(self):
        if not self.choice_made:
            self.screen.fill((255, 0, 0))  # Fill screen with red
            font = pg.font.Font(None, 74)
            text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(text, text_rect)
            
            self.character.set_direction(1)
    
            scaled_character = pg.transform.scale(self.character.current_image, 
                                                (128,240))
            char_rect = scaled_character.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(scaled_character, char_rect)
        
            pg.display.flip()
            pg.time.wait(1000)  

            game_over_texts = {
                "HIGH_SCHOOL_fighettini": "Passi i prossimi anni a frequentare feste esclusive circondato da droghe pesanti. Finisci per diventare un influencer di dubbia fama e durante un servizio fotografico su uno yacht, inciampi sul tuo ego ipertrofico e cadi in mare. Purtroppo, i tuoi 'amici' sono troppo occupati a farsi selfie per notare la tua assenza. Diventi l'ennesima vittima della superficialità.",
                "HIGH_SCHOOL_SAVONA": "Collareta decide di prenderti di mira. Scrive e pubblica online una serie di post contro di te. Piano piano il resto dei professori inizia a credere a Collareta e finiscono per denunciarti per traffico di droga.",
                "SARDINIA_MONEY": "Ti rechi al tuo ritorno a Savona presso la banca per depositarli perché rifiuti i contanti. Due giorni dopo la polizia ti porta in questura: sei sotto indagine per omicidio. La banconota era parte di un lotto di denaro trovato sulla scena di un truce omicidio tra gang mafiose rivali. Questo era l'unico loro indizio e l'omicidio era così tremendo che reintroducono la pena capitale solo per te.",
                "ARCHITECTURE": "Sei così bravo che aiuti nella ricostruzione del Ponte Morandi con Renzo Piano. Tuttavia, Renzo ti vede come un rivale e stronca la tua carriera. Finisci per dormire sotto lo stesso ponte che hai aiutato a progettare.",
                "POKER": "Sfortunatamente, perdi un sacco di soldi. Per recuperare il tuo patrimonio decidi di iniziare a vendere erba che rubi al tuo coinquilino senza che lui se ne accorga. Un giorno, però, ti trovi nel parco a fare una transazione e dietro di te compaiono 4 individui loschi che ti atterrano, ti rubano il telefono, ti chiudono il conto in banca e torni a Savona. Finalmente, finisci a lavorare per la famiglia di Elisabetta come giardiniere nella sua mega villa."
            }
            
            text = game_over_texts.get(self.game_over_reason, "Game Over")
            result = self.split_and_display_text(text, "Ci proviamo di nuovo?", ["Torna indietro", "Esci dal gioco"])
            
            if result == "Torna indietro":
                self.choice_made = True
                self.reset_to_previous_state()
            elif result == "Esci dal gioco" or result == "QUIT":
                self.running = False
            elif result is None:
                return False

        return self.running

    def reset_to_previous_state(self):
        if self.previous_state:
            self.change_state(self.previous_state)
            self.game_over_reason = None
            self.choice_made = False
            self.returning_from_game_over = True
            self.update_background() 
        else:
            self.reset()



    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen before drawing

        if self.current_stage == "FINALE_POSITIVO":
            self.handle_finale_positivo()
        else:
            self.background.draw(self.current_stage)
 
            # Always draw the character unless we're in the start screen, intro scene, or game over
            if self.current_stage not in ["START_SCREEN", "INTRO_SCENE", "GAME_OVER"]:
                self.character.draw()

            if self.current_stage == "START_SCREEN":
                self.draw_start_screen()
            elif self.current_stage == "INTRO_SCENE":
                self.intro_scene.draw()
            elif self.current_stage == "GAME_OVER":
                self.handle_game_over()
            else:
                result = self.dialogue_manager.draw()
                if result:
                    self.handle_choice_result(self.current_stage, result)
        
        pg.display.flip()
        self.clock.tick(self.fps)

    def draw_start_screen(self):
        image_rect = self.start_screen_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(self.start_screen_image, image_rect)
        self.dialogue_manager.draw_start_screen()

    def handle_choice_result(self, current_stage, result):
        if result == "QUIT":
            self.running = False
            return

        self.previous_state = current_stage

        if current_stage == "HIGH_SCHOOL_CHOICE":
            if result == "Fighettini":
                self.game_over_reason = "HIGH_SCHOOL_fighettini"
                self.change_state("GAME_OVER")
            elif result == "Peppie":
                self.change_state("AMERICA_CHOICE")
        elif current_stage == "AMERICA_CHOICE":
            if result == "Restare a Savona":
                self.game_over_reason = "HIGH_SCHOOL_SAVONA"
                self.change_state("GAME_OVER")
            elif result == "Andare in America":
                self.change_state("MOVE_TO_PEPPIE_SARDINIA")
        elif current_stage == "SARDINIA_CHOICE":
            if result == "Prima strillo un po'":
                self.change_state("UNIVERSITY_CHOICE")
            elif result == "Sì, senza problemi":
                self.game_over_reason = "SARDINIA_MONEY"
                self.change_state("GAME_OVER")
        elif current_stage == "UNIVERSITY_CHOICE":
            if result == "Legge":
                self.change_state("ROME_SCENE")
            elif result == "Architettura":
                self.game_over_reason = "ARCHITECTURE"
                self.change_state("GAME_OVER")
        elif current_stage == "ROME_SCENE":
            if result == "Scopri il poker online":
                self.game_over_reason = "POKER"
                self.change_state("GAME_OVER")
            elif result == "Ti impegni con costanza":
                self.change_state("FINALE_POSITIVO")
        elif current_stage == "FINALE_POSITIVO":
            if result == "Ricomincia":
                self.reset()
                self.change_state("START_SCREEN")
            elif result == "Esci dal gioco":
                self.running = False

        self.choice_made = False


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.current_stage == "START_SCREEN":
                        self.change_state("INTRO_SCENE")
                elif event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_a:
                    if self.current_stage == "MOVE_TO_PEPPIE" and self.dialogue_manager.can_start_conversation():
                        self.change_state("PEPPIE_DIALOGUE")
                        self.dialogue_manager.start_conversation()
                    elif self.current_stage == "MOVE_TO_PEPPIE_SARDINIA" and self.dialogue_manager.can_start_conversation():
                        self.change_state("PEPPIE_DIALOGUE_SARDINIA")
                        self.dialogue_manager.start_conversation()
                elif self.current_stage == "GAME_OVER" and event.key == pg.K_RETURN:
                    self.reset()
        return self.running
        
    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.reset_to_start_screen()
           



    def reset(self):
        self.current_stage = "START_SCREEN"
        self.start_screen_counter = 0
        self.character.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.game_over_drawn = False
        self.finale_drawn = False
        self.dialogue_manager.reset()
        self.intro_scene_done = False
        self.play_bg_sound("MAIN")
        self.choice_history = []  # Reset choice history
        self.high_school_choice_made = False  # Reset all choice flags
        self.america_choice_made = False
        self.sardinia_choice_made = False
        self.university_choice_made = False
        self.rome_choice_made = False

    def play_bg_sound(self, sound_key):
        if sound_key in self.bg_sounds:
            if not self.bg_channel.get_busy() or self.bg_channel.get_sound() != self.bg_sounds[sound_key]:
                self.bg_channel.fadeout(500)  # Fade out the current sound over 0.5 seconds
                pg.time.wait(500)  # Wait for the fadeout to complete
                self.bg_channel.play(self.bg_sounds[sound_key], loops=-1, fade_ms=1000)  # Fade in the new sound over 1 second
# Fade in the new sound over 1 second


    def update_character_movement(self):
        keys = pg.key.get_pressed()
        old_rect = self.character.rect.copy()
        is_moving = False

        if keys[pg.K_LEFT]:
            self.character.update(2, self.collision_detector)
            is_moving = True
        elif keys[pg.K_RIGHT]:
            self.character.update(3, self.collision_detector)
            is_moving = True
        elif keys[pg.K_UP]:
            self.character.update(0, self.collision_detector)
            is_moving = True
        elif keys[pg.K_DOWN]:
            self.character.update(1, self.collision_detector)
            is_moving = True

        self.character.is_walking = is_moving

        if self.current_stage == "MOVE_TO_PEPPIE":
            if self.character.rect.colliderect(self.background.group_rects["peppie"]):
                self.character.rect = old_rect
        elif self.current_stage == "MOVE_TO_PEPPIE_SARDINIA":
            if self.character.rect.colliderect(self.peppie_rect_sardinia):
                self.character.rect = old_rect

    def check_for_exit(self):
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_ESCAPE:
                self.running = False
                return True
        return False
    
    def check_conversation_triggers(self):
        for group, rect in self.background.group_rects.items():
            if self.character.rect.colliderect(rect.inflate(100, 100)):
                self.dialogue_manager.set_conversation_available(group)
                break
        else:
            self.dialogue_manager.set_conversation_available(None)