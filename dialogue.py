import pygame as pg
import time
import random
from resource_path import resource_path

class DialogueManager:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.font = pg.font.Font(resource_path("fonts/pokemon-ds-font.ttf"), 24)
        self.title_font = pg.font.Font(resource_path("fonts/pokemon-ds-font.ttf"), 36)
        self.text_color = (0, 0, 0)
        self.text_speed = 25
        self.choice_color = (0, 0, 0)
        self.choice_highlight_color = (0, 128, 255)

        self.start_underlined = False
        self.dialogue_sound = pg.mixer.Sound(resource_path("sounds/Pokemon A Button Sound.ogg"))
        self.choice_sound = pg.mixer.Sound(resource_path("sounds/Pokemon A Button Sound.ogg"))
        self.delay_timer = 0
        self.delay_duration = 3000
        
        self.game_state = game_state
        self.narrator = random.choice(["Paola", "Keisi", "Laura", "Betta"])
        self.dialogue_step = 0
        self.current_stage = "INTRO_SCENE"
        self.conversation_available = False
        self.peppie_dialogue_step = 0
        self.sardinia_dialogue_step = 0
        self.current_dialogue = None
        


    def set_game_state(self, game_state):
        self.game_state = game_state

    def update(self):
        if self.current_stage == "INTRO_SCENE":
            return self.handle_intro_scene()
        elif self.current_stage == "PEPPIE_DIALOGUE":
            return self.handle_peppie_dialogue()
        elif self.current_stage == "HIGH_SCHOOL_CHOICE":
            return self.handle_high_school_choice()
        elif self.current_stage == "AMERICA_CHOICE":
            return self.handle_america_choice()
        elif self.current_stage == "PEPPIE_DIALOGUE_SARDINIA":
            return self.handle_ppd_2()
        elif self.current_stage == "SARDINIA_CHOICE":
            return self.handle_sardinia_choice()
        elif self.current_stage == "UNIVERSITY_CHOICE":
            return self.handle_university_choice()
        elif self.current_stage == "ROME_SCENE":
            return self.handle_rome_scene()
        return None

    def handle_intro_scene(self):
        self.current_stage = "INTRO_SCENE"
        return None

    def handle_peppie_dialogue(self):
        dialogue_steps = [
            ("Laura: Lorenzo, abbiamo saputo che stai per fare un viaggio nel passato. Avresti proprio potuto invitarci.", "Cosa rispondi?", ["Lo stavo per fare", "Se proprio volete..."]),
            ("Keisi: Vi ricordo che il viaggio è in macchina, noi siamo sei e Lorenzo è l'unico che sa guidare.", "Come reagisci?", ["Giusta osservazione", "Vi dovete svegliare"]),
            ("Elisabetta: Se volete posso invitare Anna che ha la patente e magari ci porta lei.", "Cosa ne pensi?", ["Ma sti cazzi", "Sempre la stessa storia"]),
            ("Elisabetta: Però non partiamo troppo presto che ho l'estetista.", "Cosa ne pensi?", ["Rompi cazzi", "Bagagliaio per tutte"]),
            ("Paola: Beh ragazzi abbiamo tante volte escluso qualcuno dal gruppo, non vedo perché non possiamo farlo anche questa volta.", "Chi vuoi escludere?", ["Laura", "Paola"]),
            ("Ludovica: Tranquilli ragazzi, nessun problema, purtroppo ho la febbre a 40 da 515 giorni, non credo di riuscire a venire.", "Lorenzo pensa:", ["Come al solito", "Alleluia"])
        ]

        if self.peppie_dialogue_step < len(dialogue_steps):
            narrator_text, question, choices = dialogue_steps[self.peppie_dialogue_step]
            choice = self.draw_dialogue(narrator_text, question, choices)
            if choice == "QUIT":
                return "QUIT"
            if choice:
                self.peppie_dialogue_step += 1
                if self.peppie_dialogue_step == len(dialogue_steps):
                    print("Peppie dialogue complete")  # Debug print
                    return "HIGH_SCHOOL_CHOICE"
                return "CONTINUE_DIALOGUE"
        return None


    def handle_high_school_choice(self):
        narrator_text = "Davanti a te si presenta una scelta importante. Con chi vuoi passare i tuoi anni del liceo?"
        choices = ["Peppie", "Fighettini"]
        choice = self.draw_dialogue(narrator_text, "Scegli con saggezza:", choices)
        return choice if choice != "QUIT" else "QUIT"

    def handle_america_choice(self):
        narrator_text = f"{self.narrator}: Perfetto, hai scelto le persone giuste! Ma davanti a te si presenta un'altra scelta..."
        choices = ["Restare a Savona", "Andare in America"]
        choice = self.draw_dialogue(narrator_text, "Vuoi restare a Savona o andare a inseguire il tuo sogno americano?", choices)
        return choice if choice != "QUIT" else "QUIT"

    def handle_ppd_2(self):
        dialogue_steps = [
            ("Paola/Laura: Lollo il tuo American Dream si è avverato! Sei tornato in Italia da star!", "Sei Contento?", ["Ci voleva", "Moderatamente"]),
            ("Elisabetta: Che stress, ora però dobbiamo pensare alla maturità...", "Come rispondi?", ["60!!!", "Ciaone"]),
            ("Narratore: Prepari la maturità e la passi con successo, finalmente puoi goderti il frutto dei tuoi ardui sacrifici.", None, ["Continua"]),
            ("Narratore: Con le Peppie, i teatranti e il mitico Luca vi recate in Sardegna. Ma, nella terra di Paola ti si presenta una scelta difficile...", None, ["Continua"])
        ]
        
        if self.sardinia_dialogue_step < len(dialogue_steps):
            narrator_text, question, choices = dialogue_steps[self.sardinia_dialogue_step]
            choice = self.draw_dialogue(narrator_text, question, choices)
            if choice == "QUIT":
                return "QUIT"
            if choice:
                self.sardinia_dialogue_step += 1
                if self.sardinia_dialogue_step == len(dialogue_steps):
                    print("Sardinia dialogue complete")
                    return "SARDINIA_CHOICE"
                return "CONTINUE_DIALOGUE"
        return None

    def handle_sardinia_choice(self):
        narrator_text = f"{self.narrator}: Accetti o meno i 5 euro di Laura per la pizza?"
        question = "Cosa fai?"
        choices = ["Prima strillo un po'", "Sì, senza problemi"]
        choice = self.draw_dialogue(narrator_text, question, choices)
        return choice if choice != "QUIT" else "QUIT"

    def handle_university_choice(self):
        narrator_text = f"{self.narrator}: Sei proprio Lorenzo, questa storia verrà raccontata ai tuoi discendenti. Però ora davanti a te si presenta una scelta importante..."
        question = "Cosa vuoi studiare all'università?"
        choices = ["Legge", "Architettura"]
        choice = self.draw_dialogue(narrator_text, question, choices)
        return choice if choice != "QUIT" else "QUIT"

    def handle_rome_scene(self):
        narrator_text = f"{self.narrator}: Vai a Roma, conosci persone molto simpatiche (non più di noi, ma veramente chi vorrebbe essere come noi). Studi legge senza problemi, prendi voti eccellenti, fino al momento in cui l'ansia inizia a farsi sentire..."
        question = "Come affronti questo momento difficile?"
        choices = ["Scopri il poker online", "Ti impegni con costanza"]
        choice = self.draw_dialogue(narrator_text, question, choices)
        return choice if choice != "QUIT" else "QUIT"
    
    def set_dialogue(self, narrator_text, question, choices):
        self.current_dialogue = (narrator_text, question, choices)
    
    def reset_dialogue(self):
        self.dialogue_step = 0
        self.peppie_dialogue_step = 0
        self.sardinia_dialogue_step = 0

    def reset(self):
        self.current_stage = "INTRO_SCENE"
        self.conversation_available = False

    def set_conversation_available(self, group):
        self.conversation_available = group is not None
        if self.conversation_available:
            self.show_press_a_prompt()

    def can_start_conversation(self):
        return self.conversation_available and (self.current_stage in ["MOVE_TO_PEPPIE", "MOVE_TO_PEPPIE_SARDINIA"])


    def start_conversation(self):
        if self.can_start_conversation():
            if self.current_stage == "MOVE_TO_PEPPIE":
                self.current_stage = "PEPPIE_DIALOGUE"
                self.peppie_dialogue_step = 0
            elif self.current_stage == "MOVE_TO_PEPPIE_SARDINIA":
                self.current_stage = "PEPPIE_DIALOGUE_SARDINIA"
                self.sardinia_dialogue_step = 0

    def draw(self):
        if self.conversation_available and self.current_stage in ["MOVE_TO_PEPPIE", "MOVE_TO_PEPPIE_SARDINIA"]:
            self.show_press_a_prompt()
        return self.update()
    
    def draw_2(self):
        if self.current_dialogue:
            narrator_text, question, choices = self.current_dialogue
            result = self.draw_dialogue(narrator_text, question, choices)
            if result:
                self.current_dialogue = None
            return result
        return None

    def show_press_a_prompt(self):
        press_a_text = "Press A to talk"
        press_a_surface = self.font.render(press_a_text, True, (255, 255, 255))
        press_a_rect = press_a_surface.get_rect(bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20))
        self.screen.blit(press_a_surface, press_a_rect)

    def draw_start_screen(self):
        title_text = "Lorenzo's Adventure"
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_surface, title_rect)

        start_text = "Start"
        start_color = (255, 0, 0) if self.start_underlined else (255, 255, 255)
        start_surface = self.font.render(start_text, True, start_color)
        start_rect = start_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
        self.screen.blit(start_surface, start_rect)

        if self.start_underlined:
            pg.draw.line(self.screen, start_color, 
                         (start_rect.left, start_rect.bottom + 2),
                         (start_rect.right, start_rect.bottom + 2), 2)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if not self.start_underlined:
                        self.start_underlined = True
                    else:
                        return True
        return False

    def draw_game_over(self, text):
        self.draw_text_box(text)
        choice = self.draw_choice_box(["Go back"])
        if choice == "Go back":
            return True
        return False
    
    def draw_finale_positivo(self):
        narrator_text = f"Narratore: Ti laurei, con tutti i tuoi cari, degli amici che ti vogliono forse fin troppo bene e che tu ricambi distruggendoli a paintball."
        choices = ["Ricomincia", "Esci dal gioco"]
        question= "E adesso cosa vuoi fare?"
        choice = self.draw_dialogue(narrator_text, question, choices)
        return choice if choice != "QUIT" else "QUIT"
    
    def draw_dialogue(self, narrator_text, question, choices, box_size=None):
        self.draw_text_box(narrator_text)
        pg.display.flip()
        
        self.delay_timer = pg.time.get_ticks()
        
        while pg.time.get_ticks() - self.delay_timer < self.delay_duration:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return "QUIT"
            pg.time.Clock().tick(60)
        
        if question:
            self.draw_text_box(question)
        result = self.draw_choice_box(choices, box_size)
        if result == "QUIT":
            return "QUIT"
        return result

    def draw_text_box(self, text, border_color=(128, 128, 128), fill_color=(255, 255, 255), text_color=(0, 0, 0)):
        text_box_rect = pg.Rect(50, self.screen.get_height() - 150, self.screen.get_width() - 100, 100)
        pg.draw.rect(self.screen, fill_color, text_box_rect)
        pg.draw.rect(self.screen, border_color, text_box_rect, 2)
        self.animate_text(text, text_box_rect.move(10, 10), text_color)
        self.dialogue_sound.play()

    def draw_choice_box(self, choices, box_size=None):
        max_width = max(max(self.font.size(line)[0] for line in choice.split('\n')) for choice in choices)
        box_width = max(max_width + 60, 225)  

        # Calculate the total height based on the number of lines in all choices
        total_lines = sum(len(choice.split('\n')) for choice in choices)
        box_height = max(30 * total_lines + 40, 96)  # Add some padding

        # Position the box on the right side of the screen
        choice_box_rect = pg.Rect(
            self.screen.get_width() - box_width - 50,  # 20 pixels from the right edge
            350,
            box_width,
            box_height
        )
        
        selected_choice = 0
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected_choice = (selected_choice - 1) % len(choices)
                        self.choice_sound.play()
                    elif event.key == pg.K_DOWN:
                        selected_choice = (selected_choice + 1) % len(choices)
                        self.choice_sound.play()
                    elif event.key == pg.K_RETURN:
                        self.choice_sound.play()
                        running = False
                    elif event.key == pg.K_ESCAPE:
                        return "QUIT"

            pg.draw.rect(self.screen, (255, 255, 255), choice_box_rect)
            pg.draw.rect(self.screen, (128, 128, 128), choice_box_rect, 2)

            y_offset = 20
            for i, choice in enumerate(choices):
                arrow = ">" if i == selected_choice else " "
                choice_color = self.choice_highlight_color if i == selected_choice else self.choice_color
                
                lines = choice.split('\n')
                for j, line in enumerate(lines):
                    choice_text = f"{arrow} {line.strip()}" if j == 0 else f"  {line.strip()}"
                    choice_surface = self.font.render(choice_text, True, choice_color)
                    choice_rect = choice_surface.get_rect()
                    choice_rect.topleft = (choice_box_rect.left + 20, choice_box_rect.top + y_offset)
                    self.screen.blit(choice_surface, choice_rect)
                    y_offset += 30  # Increase y_offset for each line

                y_offset += 10  # Add extra space between choices

            pg.display.flip()

        return choices[selected_choice]

    def animate_text(self, text, rect, color=None):
        if color is None:
            color = self.text_color

        words = text.split(' ')
        max_width = rect.width - 20
        lines = []
        current_line = ""

        for word in words:
            if self.font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        for i, line in enumerate(lines):
            for j in range(len(line)):
                text_surface = self.font.render(line[:j+1], True, color)
                text_rect = text_surface.get_rect(topleft=(rect.left, rect.top + i * 30))
                self.screen.blit(text_surface, text_rect)
                pg.display.flip()
                time.sleep(self.text_speed / 1000)