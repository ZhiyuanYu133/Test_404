from django import forms
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from users.connect_team_a import get_team_a_posts
from .models import Post, Comment


# render(request, page to render, context)

@user_passes_test(lambda u: not u.is_authenticated, login_url='stream-home')
def welcome(request):
    return render(request, "stream/welcome.html")


@login_required
def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "stream/home.html", context)


# See if we can filter post here
class PostForm(forms.ModelForm):
    visibilityOptions = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    visibility = forms.ChoiceField(widget=forms.RadioSelect, choices=visibilityOptions)

    contentTypeOptions = (
        ('text/markdown -- common mark', 'text/markdown -- common mark'),
        ('text/plain -- UTF-8', 'text/plain -- UTF-8'),
        ('application/base64', 'application/base64'),
        (' image/png;base64', ' image/png;base64'),
        ('image/jpeg;base64', 'image/jpeg;base64'),
    )
    contentType = forms.ChoiceField(widget=forms.RadioSelect, choices=contentTypeOptions)

    class Meta:
        model = Post
        fields = ['title', 'description', 'contentType', 'content', 'image', 'categories', 'visibility', 'published']


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "stream/home.html"
    context_object_name = "posts"
    ordering = ['-published']

    def get_queryset(self):
        # Get the value of the radio button from the GET request
        queryset = Post.objects.filter(visibility='public')
        # Order the queryset by published date
        queryset = queryset.order_by('-published')
        queryset = list(queryset)
        teams_a_posts = get_team_a_posts()
        queryset.extend(teams_a_posts)
        return queryset


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    # Set post author to current login user
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    # Check if user browsing the post is the author
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    # Check if user browsing the post is the author
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


@method_decorator(login_required(login_url=reverse_lazy('welcome')), name='dispatch')
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["comment"]

    # Set post author to current login user
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Set post author to current login user
        form.instance.author = self.request.user.profile
        # Save the comment object
        response = super().form_valid(form)
        # Add the comment to the post's comments field
        post.comments.add(self.object)
        post.count += 1
        post.save()
        return super().form_valid(form)


@login_required
def about(request):
    return render(request, "stream/about.html", {'title': 'About'})
