from django.test import TestCase
from models import *

import json

# Create your tests here.

class CaravanTestCase(TestCase):
    def setUp(self):
        world = World(name="newWorld", distance_modifier=1.0 time_modifier=1.0)
        land = Land(world=world, x = 1, y = 2)
        cargo = {"resource_name": "Metal","resource_id": 0,"amount": 3}
        caravan = Caravan(domestic_cargo = json.dump(cargo), domestic_land=land, foreign_land=land)

    #def test
