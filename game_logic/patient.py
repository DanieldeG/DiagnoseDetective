# game_logic/patient.py
import random
import json
import os

class Patient:
    def __init__(self, level, completed_cases = [], dataset_path=None):
        # Default path: project-root/data/data.json
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'data.json')
        dataset_path = os.path.abspath(dataset_path)

        with open(dataset_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        # Prepare the first case
        self.completed_cases = completed_cases
        self.level = level
        self.generate_case()

    def generate_case(self):
        # Choose a random case from the loaded JSON list
        case = random.choice(self.data[self.level])

        # Keep choosing until we find a case not in completed_cases
        while case in self.completed_cases:
            case = random.choice(self.data[self.level])

        self.raw_case = case

        # Symptoms are stored as a list in the JSON
        self.symptoms = case.get('symptoms', [])

        # Disease choices (as provided in the JSON case)
        self.diseases = case.get('diseases', [])
        self.correct_disease_index = case.get('correct_disease')

        # Treatments and correct treatment index
        self.treatments = case.get('treatments', [])
        self.correct_treatment_index = case.get('correct_treatment')

        # Create shuffled options for display while keeping track of the correct one
        self.options = self.diseases.copy()
        random.shuffle(self.options)

        # Resolve which index in self.options corresponds to the correct disease
        self.correct_option = None
        if isinstance(self.correct_disease_index, int) and 0 <= self.correct_disease_index < len(self.diseases):
            correct_name = self.diseases[self.correct_disease_index]
            if correct_name in self.options:
                self.correct_option = self.options.index(correct_name)

    def get_correct_disease_name(self):
        if isinstance(self.correct_disease_index, int) and 0 <= self.correct_disease_index < len(self.diseases):
            return self.diseases[self.correct_disease_index]
        return None

    def check_disease_choice(self, choice_index):
        """Return True if the provided choice_index (index into self.options) is the correct disease."""
        return self.correct_option is not None and choice_index == self.correct_option

    def get_treatment_options(self):
        return self.treatments.copy()

    def get_correct_treatment_name(self):
        if isinstance(self.correct_treatment_index, int) and 0 <= self.correct_treatment_index < len(self.treatments):
            return self.treatments[self.correct_treatment_index]
        return None
