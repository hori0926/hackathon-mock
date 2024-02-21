from django.db import models

class DifficultyChoice(models.IntegerChoices):
    EASY = 1
    NORMAL = 2
    HARD = 3