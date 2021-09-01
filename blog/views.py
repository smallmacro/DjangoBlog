from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post



# Create your views here.
def home(request):
    context = {
        'posts' :Post.objects.all()
    }
    return render(request, 'blog/home.html' ,context)

 #default template name is <app_name>/<model_name>_viewtype.html
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'

class PostDetailView(DetailView):
    model = Post

#default template name is <app_name>/<model_name>_form.html

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    #set the form author to avoid intergrity error
    ## make sure the only login user can create post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#default template name is <app_name>/<model_name>_form.html
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Post
    fields = ['title', 'content']

    #set the form author to avoid intergrity error
    #make sure the only login user can update post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #make sure the only login user can update his own post blog
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

#default template name is <app_name>/<model_name>_confirm_delete.html
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
    model = Post
    success_url = '/'
    #set the form author to avoid intergrity error
    #make sure the only login user can update post
   
    #make sure the only login user can update his own post blog
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False




def about(request):

    return render(request, 'blog/about.html' ,{})