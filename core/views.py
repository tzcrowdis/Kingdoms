from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
import json

from .models import *

import simulation.simulation as sim
from datetime import datetime
from django.utils import timezone


"""
Administrative Functions
"""
def index(request):
    if request.user.is_authenticated:
        return faction(request, faction=Faction.objects.get(ruler=request.user))
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def faction(request, faction):

    # filter letters to only show those that have arrived
    letters = Faction.objects.get(ruler=request.user).letters.all()
    arrived = []
    for letter in letters:
        time_elapsed_in_transit = (datetime.now(tz=timezone.utc) - letter.send_time).total_seconds()
        if time_elapsed_in_transit > letter.fly_time:
            arrived.append(letter)

    # known factions
    known_factions = faction.known.all()

    # TODO: filter other objects

    return render(request, "faction.html", {
        "faction": faction,
        "letters": arrived,
        "known_factions": known_factions
        })


"""
User Actions
"""
@login_required
def send_letter(request):

    if request.method != "POST":
        return JsonResponse({"error": "request must be POST"}, status=400)

    data = json.loads(request.body)

    # TODO get the data and create the letter object
    # TODO also will need a js function to send the data

    return JsonResponse({"success": "letter sent"}, status=200)
        

"""
Login / Register functions
"""
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        # TODO: make username or email work here
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        
        # faction fields
        faction_name = request.POST["faction"]

        # attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Email or Username already taken."
            })
        login(request, user)

        # attempt to create their faction
        try:
            faction_start_vals = sim.generate_starting_values(Faction.objects.count() + 1) # +1 because we are adding a faction
            faction = Faction(
                ruler = user,
                name = faction_name,
                capital_x = faction_start_vals["x"],
                capital_y = faction_start_vals["y"],
                population = faction_start_vals["population"],
                soldiers = faction_start_vals["soldiers"],
                money = faction_start_vals["money"],
                food = faction_start_vals["food"],
                metals = faction_start_vals["metals"],
            )
            faction.save()
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Faction name already taken."
            })
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")