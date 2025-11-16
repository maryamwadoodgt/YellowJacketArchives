from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import LibraryBranch, Stock
from django.utils import translation

# Revised code with enhanced search functionality
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(
            Q(name__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(genre__icontains=search_term)
        )
    else:
        movies = Movie.objects.all()

    template_data = {
        'title': 'Movies',
        'movies': movies
    }
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    
    # Get the current language
    current_language = translation.get_language()
    
    # Get translated name, description, author, and genre
    translated_name = movie.get_translated_name(current_language)
    translated_description = movie.get_translated_description(current_language)
    translated_author = movie.get_translated_author(current_language)
    translated_genre = movie.get_translated_genre(current_language)

    template_data = {}
    template_data['title'] = translated_name
    template_data['movie'] = movie
    template_data['translated_name'] = translated_name
    template_data['translated_description'] = translated_description
    template_data['translated_author'] = translated_author
    template_data['translated_genre'] = translated_genre
    template_data['reviews'] = reviews
    template_data['current_language'] = current_language
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.rating = int(request.POST.get('rating', 0))  # Get rating from form
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.rating = int(request.POST.get('rating', review.rating))  # Keep old rating if not provided
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)


def branches_list(request):
    """Return a JSON list of all library branches with basic info."""
    branches = LibraryBranch.objects.all()
    data = []
    for b in branches:
        data.append({
            'id': b.id,
            'name': b.name,
            'address': b.address,
            'latitude': float(b.latitude) if b.latitude is not None else None,
            'longitude': float(b.longitude) if b.longitude is not None else None,
            'phone': b.phone,
        })
    return JsonResponse({'branches': data})


def movie_branches(request, id):
    """Return branches that have stock for the given movie id."""
    movie = get_object_or_404(Movie, id=id)
    stocks = Stock.objects.filter(movie=movie, count__gt=0).select_related('branch')
    data = []
    for s in stocks:
        b = s.branch
        data.append({
            'branch_id': b.id,
            'branch_name': b.name,
            'address': b.address,
            'latitude': float(b.latitude) if b.latitude is not None else None,
            'longitude': float(b.longitude) if b.longitude is not None else None,
            'phone': b.phone,
            'count': s.count,
        })
    return JsonResponse({'movie_id': movie.id, 'movie_name': movie.name, 'branches': data})