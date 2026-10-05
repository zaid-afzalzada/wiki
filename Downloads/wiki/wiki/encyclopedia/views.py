import markdown2
import random 
from django.shortcuts import render , redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)


    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get("q")

    if query in util.list_entries():
        return redirect("entry", title=query)

    results = []

    for entry in util.list_entries():
        if query.lower() in entry.lower():
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "title": title
            })

        util.save_entry(title, content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]

        util.save_entry(title, content)

        return redirect("entry", title=title)

    content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)

    return redirect("entry", title=title)