from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Author, Quote


def main(request):
    quotes = Quote.objects.filter(user=request.user).all()\
                  if request.user.is_authenticated else Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/tag.html', {'form': form})

    return render(request, 'quoteapp/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()

            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags')
                )
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            choice_author = Author.objects.filter(
                fullname__in=request.POST.getlist('authors')
                )
            for author in choice_author.iterator():
                new_quote.authors.add(author)

            return redirect(to='quoteapp:main')
        else:
            print(form.errors)
            return render(request,
                          'quoteapp/quote.html',
                          {"tags": tags, "authors": authors, 'form': form})

    return render(request,
                  'quoteapp/quote.html',
                  {"tags": tags, "authors": authors, 'form': QuoteForm()})


def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoteapp/quote_detail.html', {"quote": quote})


def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/quote_list.html', {'quotes': quotes})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to='quoteapp:main')


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request,
                          'quoteapp/author.html',
                          {'form': form})

    return render(request,
                  'quoteapp/author.html',
                  {'form': AuthorForm()})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {"author": author})


@login_required
def delete_author(request, author_id):
    Author.objects.get(pk=author_id, user=request.user).delete()
    return redirect(to='quoteapp:main')
