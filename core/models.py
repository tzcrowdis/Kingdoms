from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Faction(models.Model):
    """
    Note: ruler technically behaves one to one right now
          but in the future it could be one to many if there's different lobbies
    """
    ruler = models.ForeignKey("User", on_delete=models.CASCADE, related_name="faction")

    # faction specifics
    name = models.CharField(max_length=100, unique=True) # TODO convert white space to dashes -
    capital_x = models.IntegerField()
    capital_y = models.IntegerField()

    # resources
    population = models.IntegerField()
    soldiers = models.IntegerField()
    money = models.FloatField()
    food = models.FloatField()
    metals = models.FloatField()

    # actions
    #TODO track messages (maybe dont want to track messages), trade, scouts, and wars


class FactionKnowledge(models.Model):

    # TODO: incorporate blocks on what they know

    knower = models.ForeignKey("Faction", on_delete=models.CASCADE, related_name="knowns")
    known = models.ForeignKey("Faction", on_delete=models.CASCADE, related_name="knowers")


class Letter(models.Model):
    recipient = models.ForeignKey("Faction", on_delete=models.CASCADE, related_name="letters")
    send_time = models.DateTimeField(auto_now_add=True)
    fly_time = models.FloatField()
    message = models.CharField(max_length=200)