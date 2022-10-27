from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import is_valid_path
from .models import Review
from .forms import ReviewForm

# Create your views here.
def index(request):
    return render(request, 'reviews/index.html')

@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('reviews:community')
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/create.html', context=context)

def community(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/community.html', context)

def detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    context = {
        'review': review
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        if request == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, '글이 수정되었습니다.')
                return redirect('reviews:detail', review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            'review_form': review_form
        }
        return render(request, 'reviews/create.html', context)
    else:
        return HttpResponseForbidden()