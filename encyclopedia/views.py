from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import util
from markdown2 import Markdown
import secrets


class NewPageForm(forms.Form):

    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'placeholder': 'Please write the title' , 'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'title': 'Please use Mardown for the content','placeholder' : 'Please Write the content in markdown language', 'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):

    return render(request, "encyclopedia/index.html", {

        "entries": util.list_entries()
    })



def entry(request, entry):

    markdow_file = Markdown()
    page = util.get_entry(entry)

    if page is None:

        return render(request, "encyclopedia/404.html",{
            "entryTitle": entry
        })

    else:
        return render(request, "encyclopedia/page.html",{

        "entry": markdow_file.convert(page),

        "entryTitle": entry
        })



def newPage(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):

                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            else:
                return render(request, 'encyclopedia/newPage.html',{
                "form": form,
                "existing": True,
                "entry": title
                })
        else:
            return render(request, 'encyclopedia/newPage.html', {
                "form": form,
                "existing": False
            })
    else:
        return render(request, 'encyclopedia/newPage.html',{
            "form": NewPageForm(),
            "existing": False
        })


def edit(request, entry):
    entryPage = util.get_entry(entry)

    if entryPage is None:

        return render(request, "encyclopedia/404.html",{
            "enrtyTitle": entry
        })

    else:
        form = NewPageForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True

        return render(request, "encyclopedia/newPage.html",{
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })

def random(request):

    pages = util.list_entries()
    randomPage = secrets.choice(pages)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomPage}))


def search(request):

    text = request.GET.get('q', '')

    if util.get_entry(text) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
        
    else:
        entryString = []
        
        for entry in util.list_entries():
            if text.upper() in entry.upper():
                entryString.append(entry)
        
    return render(request, "encyclopedia/index.html", {
        "entries": entryString,
        "search": True,
        "text": text
    })