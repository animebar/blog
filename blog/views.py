from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# all the mixins must be the left of testfunctions
from django.urls import reverse_lazy
# Create your views here.

#this is a function view of home
# def home(request):
#     context = {"posts": Post.objects.all(), "title": "animesh"}
#     return render(request, "blog/home.html", context)
#this is a list view of home
class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html' #otherwise searches for <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by=5
    # it also returns a requests i.e a query set in list form

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html' #otherwise searches for <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    # here this ordering won't work as in get_queryset it is overwritten
    paginate_by=5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model=Post
# searches for <app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin, CreateView):
    # CreateView contains a form to add a post, we need to pass the author and in fields we need to mention what fields we need
    model=Post
    fields = ['title', 'content']
# searches for <app>/<model>_form.html
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy('blog-home')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    # CreateView contains a form to add a post, we need to pass the author and in fields we need to mention what fields we need
    model=Post
    fields = ['title', 'content']
    # searches for <app>/<model>_form.html which is same as create_view
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post= self.get_object()
        if post.author == self.request.user:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    def test_func(self):
        post= self.get_object()
        if post.author == self.request.user:
            return True
        return False
# expects a form that asks if you are sure to delete it
    success_url = reverse_lazy('blog-home')

def about(request):
    return render(request, "blog/about.html")
