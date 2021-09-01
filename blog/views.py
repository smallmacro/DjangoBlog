from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

# dummy data
# posts = [
#     {   
#         'author': 'macro',
#         'title': 'Blog Post 1',
#         'content' : 'First post content',
#         'date_posted' : 'August 17, 2019'
#     },

#     {   
#         'author': 'eva',
#         'title': 'Blog Post 2',
#         'content' : 'Second post content',
#         'date_posted' : 'August 27, 2019'
#     },

#     {   
#         'author': 'john',
#         'title': 'Blog Post 3',
#         'content' : 'Third post content',
#         'date_posted' : 'December 27, 2019'
#     }

# ]

# Create your views here.
def home(request):
    context = {
        'posts' :Post.objects.all()
    }
    return render(request, 'blog/home.html' ,context)


def about(request):

    return render(request, 'blog/about.html' ,{})