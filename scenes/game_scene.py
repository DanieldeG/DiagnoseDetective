import pygame
from scenes.base_scene import Scene
from settings import *
from game_logic.patient import Patient
from ui.button import Button
from scenes.fail_scene import FailScene
from scenes.succes_scene import SuccessScene

class SpeechBubble:
    def __init__(self, x, y, width, height, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text_color = (40, 40, 80)

    def draw(self, screen, text):
        lines = self.wrap_text(text, self.font, self.width - 16)
        line_height = self.font.get_linesize()
        top_padding = 45
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, self.text_color)
            screen.blit(surf, (self.x + 8, self.y + top_padding + i * (line_height + 2)))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        cur = ''
        for w in words:
            test = (cur + ' ' + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

class GameScene(Scene):
    def __init__(self, game, difficulty=None):
        # safe background load
        try:
            bg = pygame.image.load('images/patient_background.png')
        except Exception:
            bg = None
        super().__init__(game, background_image=bg)
        self.game = game
        # total / passing rules
        self.total_cases = 10
        self.required_to_pass = 7

        # score and progress
        self.case_count = 0
        self.score = 0

        # difficulty resolution: param -> game.level -> 'medium'
        self.difficulty = difficulty or getattr(game, 'level', 'medium')

        # UI state
        self.stage = 'disease'
        self.selected_option = None
        self.selected_treatment = None
        self.buttons = []
        self.speech_bubble = SpeechBubble(320, 40, 400, 120, getattr(self, 'small_font', self.font))

        # prepare first patient
        self._prepare_new_patient()

    def _prepare_new_patient(self):
        # end-of-exam check
        if self.case_count >= self.total_cases:
            if self.score >= self.required_to_pass:
                self.game.change_scene(lambda g: SuccessScene(g, self.score, self.total_cases, difficulty=self.difficulty))
            else:
                self.game.change_scene(lambda g: FailScene(g, self.score, self.total_cases, difficulty=self.difficulty))
            return

        # create patient (try passing difficulty if Patient supports it)
        try:
            self.patient = Patient(difficulty=self.difficulty)
        except TypeError:
            try:
                self.patient = Patient(self.difficulty)
            except Exception:
                self.patient = Patient()

        self.stage = 'disease'
        self.selected_option = None
        self.selected_treatment = None
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        button_w = 320
        button_h = 48
        gap = 14
        start_x = 400
        start_y = 300

        if self.stage == 'disease':
            options = getattr(self.patient, 'options', ["No options"])
        else:
            # try method then fallback attribute
            try:
                options = self.patient.get_treatment_options()
            except Exception:
                options = getattr(self.patient, 'treatments', ["No treatments"])

        for idx, opt in enumerate(options):
            def make_cb(i=idx):
                return lambda: self.select_option(i)
            btn = Button(
                text=str(opt),
                x=start_x + button_w // 2,
                y=start_y + idx * (button_h + gap),
                callback=make_cb(),
                width=button_w,
                height=button_h
            )
            self.buttons.append(btn)

    def select_option(self, idx):
        if self.stage == 'disease':
            self.selected_option = idx
            ok = False
            try:
                ok = self.patient.check_disease_choice(idx)
            except Exception:
                ok = False
            if ok:
                self.stage = 'treatment'
                self.selected_option = None
                self.create_buttons()
            else:
                self.case_count += 1
                self._prepare_new_patient()
        elif self.stage == 'treatment':
            self.selected_treatment = idx
            correct_idx = getattr(self.patient, 'correct_treatment_index', 0)
            if idx == correct_idx:
                self.score += 1
            self.case_count += 1
            self._prepare_new_patient()

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)

        # score / progress / difficulty
        score_surf = self.font.render(f"Score: {self.score}", True, (60,60,60))
        screen.blit(score_surf, (SCREEN_WIDTH - score_surf.get_width() - 16, 16))

        case_surf = self.font.render(f"Case: {min(self.case_count + 1, self.total_cases)}/{self.total_cases}", True, (60,60,60))
        screen.blit(case_surf, (16, 16))

        diff_surf = self.font.render(f"Difficulty: {self.difficulty.title()}", True, (60,60,60))
        screen.blit(diff_surf, (16, 44))

        # symptoms
        symptoms = getattr(self.patient, 'symptoms', ["No symptoms"])
        symptoms_text = "I am feeling: " + ", ".join(symptoms)
        self.speech_bubble.draw(screen, symptoms_text)

        # buttons
        for i, btn in enumerate(self.buttons):
            if self.stage == 'disease':
                btn.color = (180, 220, 180) if self.selected_option == i else BLUE
            else:
                btn.color = (180, 180, 220) if self.selected_treatment == i else GREEN
            btn.draw(screen)

        # two-line instructions
        if self.stage == 'disease':
            lines = ["Click on the disease you think", "matches the patient's symptoms!"]
        else:
            lines = ["Now choose the best treatment", "for this patient!"]
        line_spacing = self.font.get_linesize() + 4
        instr_x = 300
        instr_y = 200
        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (60,60,60))
            screen.blit(surf, (instr_x, instr_y + i * line_spacing))