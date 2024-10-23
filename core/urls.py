from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # action post urls
    path("send_letter", views.send_crow_letter, name="send_crow_letter"),

    # game pages
    path("<str:faction_name>", views.faction, name="faction"),

    # bureaucratic
    path("", views.index, name="index"),
]