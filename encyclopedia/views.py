from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
from .forms import NewPageForm, EditPageForm

import re
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """
    Render a page that displays the contents of that encyclopedia entry.
    """

    # Get the content of the title
    content = util.get_entry(title)
    
    # If title does not exist
    if not content:
        return render(request, "encyclopedia/error.html", status=404)

    # If title exists
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


def search(request):
    """
    Allows user to search for an encyclopedia entry.
    """
    
    # Get the search query
    query = request.GET['q']

    # if query is empty
    if query.strip() == "":
        return HttpResponseRedirect(reverse("wiki:index"))

    # If query exists, render entry page
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": query}))

    # If the query does not match any encyclopedia entry
    # Match all entries that have query as a substring
    p = re.compile(rf'{query.strip()}', re.IGNORECASE)
    results = [entry for entry in util.list_entries() if p.search(entry)]
    
    # Render search results page
    return render(request, "encyclopedia/search_results.html", {
        "results": results
    })


def new_page(request):
    """
    Render page where user can create an new encyclopedia entry.
    """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get the submitted form
        form = NewPageForm(request.POST)
        
        # Ensure form is valid
        if form.is_valid():

            # Get form input
            title = form.cleaned_data["title"].strip()
            
            # If title does not exist, save the new entry
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            # Redirect to the new entry's page
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })


    # User reached route via GET (as by clicking a link or via redirect)
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })


def edit_page(request, title):

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get the submitted form
        form = EditPageForm(request.POST)

        # Ensure form is valid
        if form.is_valid():

            # Get form input
            content = form.cleaned_data["content"]

            # Save edited markdown entry
            util.save_entry(title, content)

            # Redirect to the entry's page
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))

    # User reached route via GET (as by clicking a link or via redirect)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": EditPageForm(initial={"content": util.get_entry(title)})
    })


def random_page(request):
    
    # Pick a random entry from the list of entries
    entry = random.choice(util.list_entries())
    
    # Redirect to randomly picked entry's page
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": entry}))