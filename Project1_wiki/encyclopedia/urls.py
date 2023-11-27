from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("results", views.results, name="results"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("rando", views.rando, name="rando")
]
