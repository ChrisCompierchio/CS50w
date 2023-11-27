from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.new_login, name="new_login"),
    path("logout", views.new_logout, name="new_logout"),
    path("register", views.register, name="register"),
    path("new_note", views.new_note, name="new_note"),
    path("get_notes", views.get_notes, name="get_notes"),
    path("deleteNote/<str:note_id>", views.deleteNote, name="deleteNote")
]
