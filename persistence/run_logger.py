
from persistence.mongo.experience_repo import ExperienceRepository

class RunLogger:

    def __init__(self):

        self.exp_repo = ExperienceRepository()
    
    def log_experiences(self, experience_document):

        self.exp_repo.insert_game_experience(experience_document)