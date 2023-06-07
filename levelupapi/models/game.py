from django.db import models
from django.core.validators import MinValueValidator


class Game(models.Model):
    """_summary_

    Args:
        models (_type_): _description_
    """

    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    number_of_players = models.IntegerField(validators=[MinValueValidator(1)])
    skill_level = models.IntegerField()
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, default=1)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
