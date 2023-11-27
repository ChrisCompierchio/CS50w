from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def converter(mdpage):
    page = util.get_entry(mdpage)
    if page == None:
        return None
    else:
       converted = Markdown().convert(page)
       return converted

def title(request, title):
    if converter(title) == None:
        return render(request, "encyclopedia/none.html")
    else:
        return render(request, "encyclopedia/title.html", {
            "page_title": title,
            "contents": converter(title)
        })

def results(request):
    if request.method == "POST":
        text = request.POST['q']
        page = converter(text)
        results = []
        if page == None:
            for entry in util.list_entries():
                if text.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/results.html", {
                "entries": results
            })
        elif page is not None:
            return render(request, "encyclopedia/title.html", {
            "page_title": text,
            "contents": converter(text)
        })
    else:
        return render(request, "encyclopedia/results.html")

def new(request):
    if request.method == "POST":
        name = request.POST['name']
        content = request.POST['content']

        if name in util.list_entries():
             return render(request, "encyclopedia/exists.html")
        else:
            util.save_entry(name, content)
            return render(request, "encyclopedia/title.html", {
            "page_title": name,
            "contents": content
            })
    else:
        return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html")
    else:
        name = request.POST['title']
        content = util.get_entry(name)
        if content == None:
            return render(request, "encyclopedia/none.html")
        else:
            return render(request, "encyclopedia/edit.html", {
            "name": name,
            "contents": content
            })

def save(request):
    if request.method == "POST":
        name = request.POST['name']
        content = request.POST['content']
        util.save_entry(name, content)
        new_content = converter(name)
        return render(request, "encyclopedia/title.html", {
            "page_title": name,
            "contents": new_content
            })
    else:
        return render(request, "encyclopedia/edit.html")

def rando(request):
    entry = random.choice(util.list_entries())
    page = converter(entry)
    return render(request, "encyclopedia/title.html", {
            "page_title": entry,
            "contents": page
            })
