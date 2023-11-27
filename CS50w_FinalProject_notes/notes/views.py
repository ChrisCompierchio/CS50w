from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import User, Note

# Create your views here.
def index(request):
    notes = Note.objects.all()
    user_notes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    for note in notes:
        if note.author.username == request.user.username:
            if note.position:
                user_notes[note.position] = note

    return render(request, "index.html", {
        "note1": user_notes[1],
        "note2": user_notes[2],
        "note3": user_notes[3],
        "note4": user_notes[4],
        "note5": user_notes[5],
        "note6": user_notes[6],
        "note7": user_notes[7],
        "note8": user_notes[8],
        "note9": user_notes[9],
        "note10": user_notes[10],
        "note11": user_notes[11],
        "note12": user_notes[12],
        "note13": user_notes[13],
        "note14": user_notes[14],
        "note15": user_notes[15]
    })

def new_login(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def new_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

@csrf_exempt
def new_note(request):
    if request.method == "POST":
        data = json.loads(request.body)

        note_content = data.get("content")
        note_position = data.get("position")
        note_color = data.get("color")

        note = Note(author = request.user, text = note_content, position = note_position, color = note_color)
        note.save()

        return JsonResponse({"message": "Email sent successfully."}, status=201)


@csrf_exempt
def get_notes(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(note.serialize())

@csrf_exempt
def deleteNote(request, note_id):

    new_note = Note.objects.get(position = note_id, author = request.user)
    new_note.delete()

    return HttpResponseRedirect(reverse(index))
