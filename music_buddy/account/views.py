from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from music_buddy_app.forms import *
from .forms import *
import random
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

def logout_user(request):
    try:
        del request.session['user']
        logout(request)
    except:
        logout(request)
        return redirect('/')
    logout(request)
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(86400) #sets the exp. value of the session 
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

@login_required
def create_blog(request):
    # user = request.user
    # if not user.is_authenticated:
    #     return redirect("/login")
    # form = CreateBlogPostForm(request.POST or None)
    # if form.is_valid():
    #     obj = form.save(commit=False)
    #     author = user.username
    #     obj.author = author
    #     obj.save()
    #     form = CreateBlogPostForm()
    # context['form'] = form
    # return render(request, 'create_blog.html', context)
    if request.method == 'POST':
        form = CreateBlogPostForm(request)
        title = form.data._post['title']
        body = form.data._post['body']
        # post = Post(title, request.user.username,body)
        author = request.user
        Post.objects.create(title = title, author= author, body = body)
    form = CreateBlogPostForm()
    return render(request, 'create_blog.html', {'form':form})

""" 
https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d

Friend Request methods
"""

def send_friend_request(request, userID):
    if request.user.id == userID:
        return redirect('friends')
    from_user = request.user
    to_user = Account.objects.get(id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return redirect('friends')
    else:
        return redirect('friends')

def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:        
        friend_request.to_user.friends_list.add(friend_request.from_user)
        friend_request.from_user.friends_list.add(friend_request.to_user)
        friend_request.delete()
    return redirect('received')

# Since it deletes cascade, the other user's field is updated as well
def decline_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.from_user == request.user or friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('received')

# I think I could Ajax here but I'm too lazy to figure out how to reload the current window
def remove_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.from_user == request.user or friend_request.to_user == request.user:
        friend_request.delete()
    return redirect('sent')

# Since it deletes cascade, the other user's field is updated as well
def remove_friend(request, requestID):
    target_friend = Account.objects.get(id=requestID)    
    target_friend.friends_list.remove(request.user.id)
    return redirect('friends')

def edit_profile_comment(request, commentID):
    curr_user = request.user
    post = ProfileComment.objects.get(id=commentID)
    if curr_user != post.author:
        return redirect('profile' , post.webpage)
    else:
        if request.method == 'POST':
            form = EditCommentForm(request.POST)
            if form.is_valid():
                body = request.POST.get('body', '')
                
                
                post.body = body
                post.save()
            form = EditCommentForm()
            return redirect('profile' , curr_user)
        else:
            post =  get_object_or_404(ProfileComment, id=commentID)
            
            form = EditCommentForm(post)
            return render(request, 'edit_profile_comment.html' , {'post' : post, 'form': form} )

def edit_song_comment(request, songID, commentID):
    curr_user = request.user
    post = SongComment.objects.get(id=commentID)
    if curr_user != post.author:
        return redirect('comments' , songID)
    else:
        if request.method == 'POST':
            form = EditCommentForm(request.POST)
            if form.is_valid():
                body = request.POST.get('body', '')
                
                post.body = body
                post.save()
            form = EditCommentForm()
            return redirect('comments' , songID)
        else:
            post =  get_object_or_404(SongComment, id=commentID)
            form = EditCommentForm(post)
            return render(request, 'edit_profile_comment.html' , {'post' : post, 'form': form} )
