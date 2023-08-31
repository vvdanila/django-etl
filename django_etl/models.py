from django.db import models


class MalePlayer(models.Model):
    player_id = models.PositiveIntegerField()
    player_url = models.CharField(max_length=2000)
    fifa_version = models.PositiveIntegerField()
    fifa_update = models.PositiveIntegerField()
    fifa_update_date = models.DateField()
    short_name = models.CharField(max_length=50)
    long_name = models.CharField(max_length=100)
    player_positions = models.CharField(max_length=100)
    overall = models.PositiveIntegerField()
    potential = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.short_name}"
