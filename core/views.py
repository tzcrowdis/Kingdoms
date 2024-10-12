from django.shortcuts import render, redirect, HttpResponseRedirect
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
    # TODO have index and then faction accept a message variable to display success and error messages to users
    if request.user.is_authenticated:
        faction_name = Faction.objects.get(ruler=request.user).name.replace(" ", "-") # replace avoids ugly urls
        return redirect(faction, faction_name=faction_name)
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def faction(request,  faction_name):

    # TODO handle the errors does not exist and multiple objects returned
    faction = Faction.objects.get(ruler=request.user) # HACK redundant look up but couldnt pass through due to url dispatch

    # filter letters to only show those that have arrived
    #letters = Faction.objects.get(ruler=request.user).letters.all()
    letters = faction.letters.all()
    arrived = []
    for letter in letters:
        time_elapsed_in_transit = (datetime.now(tz=timezone.utc) - letter.send_time).total_seconds()
        if time_elapsed_in_transit > letter.fly_time:
            arrived.append(letter)

    # known factions
    faction_knowledge = faction.knowns.all()
    known_factions = [known.known for known in faction_knowledge]

    # get all faction scouts
    # check if scouts have returned
    # then generate reports
    scouts = faction.scouts.all()
    
    for scout in scouts:
        if scout.active:
            if datetime.now(tz=timezone.utc) > scout.return_time:
                try:
                    faction.soldiers += 1
                    faction.save()

                    scout.active = False
                    scout.save()
                except Exception as e:
                    print("failed to return scout to soldier pool")
                    print(e)
    
    scout_reports = []
    for scout in scouts:
        if scout.active:
            continue

        all_knowledge = scout.scout_knowledge.all()
        for knowledge in all_knowledge:
            scout_reports.append(sim.land_snapshot(knowledge.land, knowledge.visit_time))


    # TODO: filter other objects

    return render(request, "faction.html", {
        "faction": faction,
        "letters": arrived,
        "known_factions": known_factions,
        "scout_reports": scout_reports,
        })


"""
User Actions
"""
def send_crow_letter(request):

    if request.method != "POST":
        print("request must be POST")
        return HttpResponseRedirect(reverse("index"))

    if request.POST["recipient"] == "none":
        print("no recipient selected")
        return HttpResponseRedirect(reverse("index"))

    try:
        # get the data and create the letter object
        # HACK a javascript method may be better
        recipient_user = User.objects.get(username=request.POST["recipient"])
        recipient_obj = Faction.objects.get(ruler=recipient_user)
        recipient_loc = [recipient_obj.capital_x, recipient_obj.capital_y]

        sender_obj = Faction.objects.get(ruler=request.user)
        sender_loc = [sender_obj.capital_x, sender_obj.capital_y]

        letter = Letter(
            recipient = recipient_obj,
            fly_time = sim.crow_letter(sender=sender_loc, recipient=recipient_loc),
            message = request.POST["message"]
        )
        letter.save()

        print("successfully sent letter")
        return HttpResponseRedirect(reverse("index"))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse("index"))   
    

def send_scout(request):

    if request.method != "POST":
        print("request must be POST")
        return HttpResponseRedirect(reverse("index"))

    faction = Faction.objects.get(ruler=request.user)

    # scouts always start from the capital
    starting_position = [faction.capital.x, faction.capital.y]

    # translate the direction
    if request.POSt["direction"] == "N": # TODO add to form
        direction = (0, 1)
    elif request.POSt["direction"] == "NE":
        direction = (1, 1)
    elif request.POSt["direction"] == "E":
        direction = (1, 0)
    elif request.POSt["direction"] == "SE":
        direction = (1, -1)
    elif request.POSt["direction"] == "S":
        direction = (0, -1)
    elif request.POSt["direction"] == "SW":
        direction = (-1, -1)
    elif request.POSt["direction"] == "W":
        direction = (-1, 0)
    elif request.POSt["direction"] == "NW":
        direction = (-1, 1)
    else:
        print("must supply direction")
        return HttpResponseRedirect(reverse("index"))
    
    # total trip (there and back) specified by user
    trip_time = request.POST["travel_time"] # TODO add to form
    time_modifier = faction.world.time_modifier

    # returns a list of destinations in the form [(x, y), t]
    # where t is the time to travel from the previous node to that one
    itinerary = sim.scouting(start=starting_position, direction=direction, total_time=trip_time, dist_mod=faction.world.distance_modifier)

    # take scout from soldier pool
    try:
        faction.soldiers -= 1
        faction.save()
    except Exception as e:
        print("failed to take scout from soldier pool")
        print(e)
        return HttpResponseRedirect(reverse("index"))
    
    # create scout object
    try: 
        start_time = datetime.now(tz=timezone.utc)
        scout = Scout(
            faction = faction,
            # NOTE assumes the time the model is created and the sim function ran are approximately equal
            return_time = sim.get_real_time(start = start_time, duration = trip_time, time_mod = time_modifier),
            active = True,
        )
        scout.save()
    except Exception as e:
        print("failed to create scout")
        print(e)
        return HttpResponseRedirect(reverse("index"))
    
    # create scout knowledge from itinerary
    try:
        start_time = scout.leave_time
        for place in itinerary:
            scout_knowledge = ScoutKnowledge(
                scout = scout,
                land = Land.objects.get(x = place[0][0], y = place[0][1]),
                visit_time = sim.get_real_time(start = start_time, duration = place[1], time_mod = time_modifier),
            )
            scout_knowledge.save()
            start_time = scout_knowledge.visit_time

    except Exception as e:
        print("failed to create scout knowledge")
        print(e)
        return HttpResponseRedirect(reverse("index"))
    
    print("successfully sent scout")
    return HttpResponseRedirect(reverse("index"))


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
            # TODO rework for land model
            faction_start_vals = sim.generate_starting_values(Faction.objects.count() + 1) # +1 because we are adding a faction
            
            faction = Faction(
                ruler = user,
                name = faction_name,
                # TODO rework for land model
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