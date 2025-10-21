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
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=20)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=20)
        wrapped = self.wrap_text(text, self.font, self.rect.width - 20)
        for i, line in enumerate(wrapped):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 15 + i * (FONT_SIZE + 2)))

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
        super().__init__(game)
        self.patient = Patient()
        self.selected_option = None
        self.selected_treatment = None
        self.stage = 'disease'  # 'disease' or 'treatment'
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.large_font = pygame.font.Font(FONT_NAME, FONT_SIZE + 8)
        self.speech_bubble = SpeechBubble(200, 100, 500, 120, self.font)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        start_x = 380
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
                from scenes.fail_scene import FailScene
                self.game.change_scene(lambda game: FailScene(game, message="Incorrect disease!"))
        elif self.stage == 'treatment':
            self.selected_treatment = idx
            if idx == self.patient.correct_treatment_index:
                print("Correct treatment!")
                # You can add win logic or next patient logic here
            else:
                from scenes.fail_scene import FailScene
                self.game.change_scene(lambda game: FailScene(game, message="Incorrect treatment!"))

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(WHITE)
        # Draw patient avatar (simple circle for now)
        avatar_center = (120, 180)
        pygame.draw.circle(screen, (200, 170, 140), avatar_center, 60)
        pygame.draw.circle(screen, (0, 0, 0), avatar_center, 60, 2)
        # Draw face features
        pygame.draw.circle(screen, (0, 0, 0), (avatar_center[0]-20, avatar_center[1]-10), 8)  # left eye
        pygame.draw.circle(screen, (0, 0, 0), (avatar_center[0]+20, avatar_center[1]-10), 8)  # right eye
        pygame.draw.arc(screen, (0, 0, 0), (avatar_center[0]-20, avatar_center[1]+10, 40, 20), 3.14, 0, 2)  # smile

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
