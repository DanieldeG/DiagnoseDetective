# scenes/game_scene.py
import pygame
from scenes.base_scene import Scene
from settings import *
from game_logic.patient import Patient
from ui.button import Button
from scenes.fail_scene import FailScene

class SpeechBubble:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.bg_color = (240, 240, 255)
        self.border_color = (180, 180, 220)
        self.text_color = (40, 40, 80)

    def draw(self, screen, text):
        wrapped = self.wrap_text(text, self.font, self.rect.width - 20)
        for i, line in enumerate(wrapped):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 15 + i * (SMALL_FONT_SIZE + 2)))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current = ''
        for word in words:
            test = current + word + ' '
            if font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current.strip())
                current = word + ' '
        if current:
            lines.append(current.strip())
        return lines

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game, background_image=pygame.image.load('images/patient_background.png'))
        self.buttons = []
        self._prepare_new_patient()
        self.speech_bubble = SpeechBubble(350, 60, 350, 120, self.small_font)
        self.score = 0
    
    def _prepare_new_patient(self):
        self.patient = Patient()
        self.stage = 'disease'
        self.selected_option = None
        self.selected_treatment = None
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        start_x = SCREEN_WIDTH // 2
        start_y = 275
        button_w = 320
        button_h = 50
        gap = 18
        options = self.patient.options if self.stage == 'disease' else self.patient.get_treatment_options()
        for idx, option in enumerate(options):
            def make_callback(i=idx):
                return lambda: self.select_option(i)
            btn = Button(
                text=option,
                x=start_x + button_w // 2,
                y=start_y + idx * (button_h + gap),
                callback=make_callback(),
                width=button_w,
                height=button_h
            )
            self.buttons.append(btn)

    def select_option(self, idx):
        if self.stage == 'disease':
            self.selected_option = idx
            if self.patient.check_disease_choice(idx):
                self.stage = 'treatment'
                self.selected_option = None
                self.create_buttons()
            else:
                self.game.change_scene(lambda game: FailScene(game, message="Incorrect disease!"))
        elif self.stage == 'treatment':
            self.selected_treatment = idx
            if idx == self.patient.correct_treatment_index:
                self.score += 1
                self._prepare_new_patient()
            else:
                self.game.change_scene(lambda game: FailScene(game, message="Incorrect treatment!"))

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)

        # Draw the score
        score_text = self.font.render(f"Score: {self.score}", True, (60, 60, 60))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

        # Draw speech bubble for symptoms
        symptoms_text = "I am feeling: " + ", ".join(self.patient.symptoms)
        self.speech_bubble.draw(screen, symptoms_text)

        # Draw options as buttons
        for idx, btn in enumerate(self.buttons):
            if self.stage == 'disease':
                btn.color = (180, 220, 180) if self.selected_option == idx else BLUE
            else:
                btn.color = (180, 180, 220) if self.selected_treatment == idx else GREEN
            btn.draw(screen)

        # Instructions
        if self.stage == 'disease':
            instr = self.font.render("Click on the disease you think matches the patient's symptoms!", True, (60, 60, 60))
        else:
            instr = self.font.render("Now choose the best treatment for this patient!", True, (60, 60, 60))
        screen.blit(instr, (380, 235))
