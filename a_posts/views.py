from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post, Response
from .forms import PostCreateForm, ResponseCreateForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q

# Create your views here.

def home(request, category=None, author=None):
    selected_category = category
    posts = Post.objects.all()

    if category:
        posts = posts.filter(category=category)

    if author:
        posts = posts.filter(author__username=author)  # Фильтрация по автору

    top_authors = User.objects.annotate(like_count=Count('post__likes')).filter(like_count__gt=0).order_by('-like_count')[:3]
    author_filter = Post.objects.filter(author__username=request.user.username)
    categories = Post.TYPE

    context = {
        'posts': posts,
        'top_authors': top_authors,
        'categories': categories,
        'selected_category': selected_category,
        'author_filter': author_filter
    }  

    return render(request, 'a_posts/home.html', context)



def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('home')
    return render(request, 'a_posts/post_create.html', {'form': form})

def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post': post})

def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostCreateForm(instance=post)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited')
            return redirect('home')
    context = {'form': form, 'post': post}         
    return render(request, 'a_posts/post_edit.html', context)

def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    responseform = ResponseCreateForm()
    categories = Post.TYPE
    top_likes = Post.objects.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')

    context = {'post': post, 'responseform': responseform, 'full_text': True, 'categories': categories, 'top_likes': top_likes}

    return render(request, 'a_posts/post_page.html', context)


def send_response_notification_email(recipient_email, post_title, post_url, site_url):
    subject = 'Новый отклик на ваш пост'
    message = render_to_string('email/notification_email.html', {'post_title': post_title, 'post_url': post_url, 'site_url': site_url})
    sender_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, sender_email, [recipient_email])

@login_required
def respone_sent(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = ResponseCreateForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.parent_post = post
            response.save()   

            send_response_notification_email(post.author.email, post.title, post.get_absolute_url(), settings.SITE_URL)

    return render(request, 'snippets/add_response.html', {'response': response, 'post': post})


@login_required
def response_delete(request, pk):
    post = get_object_or_404(Response, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('post', post.parent_post.pk)
    
    return render(request, 'a_posts/response_delete.html', {'response': post})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_exist = post.likes.filter(pk=request.user.pk).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:    
            post.likes.add(request.user)

    return render(request, 'snippets/likes.html', {'post': post})


def accept_response(request, pk):
    called_response = Response.objects.get(pk=pk)
    called_response.status = True
    called_response.save()

    if called_response.author.email:
        subject = 'Ваш отклик принят'
        context = {'response': called_response, 'site_url': settings.SITE_URL}
        message = render_to_string('email/response_accepted_email.html', context)
        plain_message = strip_tags(message)
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = called_response.author.email
        send_mail(subject, plain_message, sender_email, [recipient_email], html_message=message)

    return render(request, 'snippets/accepted_response_fragment.html')
    
    
    

def delete_response(request, pk):
    called_response = Response.objects.get(pk=pk)
    called_response.delete()
    return redirect('user_responses')



@login_required
def user_responses(request):
    user_posts = Post.objects.filter(author=request.user)
    user_responses = Response.objects.filter(parent_post__in=user_posts).exclude(author=request.user)
    
    query = request.GET.get('q')
    if query:
        user_responses = user_responses.filter(Q(content__icontains=query) | Q(parent_post__title__icontains=query))
    
    context = {
        'user_responses': user_responses
    }

    return render(request, 'a_posts/user_responses.html', context)
