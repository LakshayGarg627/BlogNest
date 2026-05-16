from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
# from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User


class PostListView(ListView):
    model=Post
    template_name='blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

def about(request):
    return render(request,"blog/about.html",{'title':'About'})

def topic(request, topic_name):
    
    topic_info = {
        'python': {'icon': 'fa-python', 'color': '#3b82f6', 'title': 'Python', 'desc': 'The heart of Django. Explore Python tips, best practices, and backend logic.'},
        'javascript': {'icon': 'fa-js', 'color': '#eab308', 'title': 'JavaScript', 'desc': 'Everything from vanilla JS to React, Vue, and frontend magic.'},
        'backend': {'icon': 'fa-server', 'color': '#10b981', 'title': 'Backend', 'desc': 'Databases, APIs, architecture, and scalable system design.'},
        'frontend': {'icon': 'fa-desktop', 'color': '#ef4444', 'title': 'Frontend', 'desc': 'CSS, HTML, UI/UX, and making beautiful user interfaces.'},
        'ai': {'icon': 'fa-robot', 'color': '#a855f7', 'title': 'AI & ML', 'desc': 'Artificial Intelligence, Machine Learning, and the future of tech.'},
    }
    
    info = topic_info.get(topic_name.lower(), {
        'icon': 'fa-hashtag', 'color': 'var(--brand-purple)', 'title': topic_name.capitalize(), 'desc': f'Explore all discussions about {topic_name}.'
    })
    
    
    query = Q(title__icontains=topic_name) | Q(content__icontains=topic_name)
    meaningful_posts = Post.objects.filter(query).order_by('-date_posted')
    
    context = {
        'topic_name': topic_name,
        'info': info,
        'posts': meaningful_posts 
    }
    return render(request, "blog/topic.html", context)

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Post
    fields=["title","content"]
    success_message = "Your post has been created successfully!"

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model=Post
    fields=["title","content"]
    success_message = "Your post has been updated successfully!"

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if(post.author == self.request.user):
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/blog/'
    
    def form_valid(self, form):
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if(post.author == self.request.user):
            return True
        return False
    
    
class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')