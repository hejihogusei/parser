import random

class BackupService:
    def __init__(self):
        self._backups = []

    def save(self, model_dict):
        self._backups.append(model_dict.copy())

    def restore(self):
        if not self._backups:
            return None
        random.shuffle(self._backups)
        return self._backups.pop()
