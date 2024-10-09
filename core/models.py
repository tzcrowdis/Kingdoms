from django.db import models
from django.contrib.auth.models import AbstractUser

import random


"""
World models
"""
class World(models.Model):
    name = models.CharField(max_length=100)
    distance_modifier = models.FloatField() # how far away grid points are in kilometers
    time_modifier = models.FloatField() # how time moves relative to real time
    creation_time = models.DateTimeField(auto_now_add=True)


class Land(models.Model):
    world = models.ForeignKey("World", on_delete=models.CASCADE, related_name="land_points")
    x = models.IntegerField()
    y = models.IntegerField()

    # TODO add other land speific fields (garrisoned soldiers, population, etc)

    # TODO add resources
    RESOURCES = (
        ("MT", "Metal"),
        ("FD", "Food"),
    )
    resource = models.CharField(choices=RESOURCES, max_length=2)

    # overwrite save() to randomly allocate resource to land on creation
    def save(self, *args, **kwargs):
        self.resource = random.choice(self.RESOURCES)[0]
        super().save(*args, **kwargs)


"""
Ruler models
"""
class User(AbstractUser):
    pass


class Faction(models.Model):
    """
    Note: ruler technically behaves one to one right now
          but in the future it could be one to many if there's different lobbies
    """
    ruler = models.ForeignKey("User", on_delete=models.CASCADE, related_name="faction")
    world = models.ForeignKey("World", on_delete=models.CASCADE, related_name="factions")

    # faction specifics
    name = models.CharField(max_length=100, unique=True) # TODO convert white space to dashes -
    capital = models.ForeignKey("Land", on_delete=models.CASCADE, related_name="capitals")

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


class Scout(models.Model):
    completion_time = models.FloatField()
    # TODO finish


class ScoutKnowledge(models.Model):
    scout = models.ForeignKey("Scout", on_delete=models.CASCADE, related_name="scout_knowledge")
    # TODO finish
