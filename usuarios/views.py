from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from .forms import profileForm, UserProfile
from core.forms import PostCreation, HistoryCreation
from core.models import SavePost, Post, Histories
from core.utils import createNotifications
from django.contrib import messages
from inbox.models import Message


def session_login(request):
    loginPage = True
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = name, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('---------------------------------------------')
            messages.error(request, 'El usuario o la contrasela son incorretos')

    return render (request, 'usuarios/session-login.html', {'login' : loginPage})

def session_logOut(request):
    logout(request)
    return redirect ('login')

def session_register(request):
    loginPage = False
    form = profileForm()
    if request.method == 'POST':
        form = profileForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user = user,
                name = user.first_name,
                email = user.email
            )
            me = Profile.objects.get(id = 1)
            post = Post.objects.get(id = 1)
            Message.objects.create( sender = me, received = profile, postsended = post )
            
            Message.objects.create( sender = me, received = profile, body = f'Bienvenido "{profile.name}", cualquier consulta no dudes en preguntar')
            
            login(request, user)
            return redirect('home')
    return render (request, 'usuarios/session-login.html', {
        'login' : loginPage, 'form' : form,
        })

# perfil del usuario
@csrf_exempt
def profile_page(request, pk):
    try:
        user = User.objects.get(id = pk)
        profile = Profile.objects.get(user = user)
        post = Post.objects.filter(host = profile)
        savedPost = SavePost.objects.filter(user = user)
        postTagged = Post.objects.filter(tagged = user)
        storyUser = Histories.objects.filter(user = profile)
        if not savedPost:
            savedPost = []
    except:
        return redirect('login')
    if request.method == 'POST':
        if request.user.is_authenticated:
            action = request.POST.get('action')
            if request.user != user:
                me = Profile.objects.get(user = request.user)
                if action == 'Follow':
                    me.follow.add(user)
                    profile.followers.add(request.user)
                    createNotifications(request.user, user, type=1, post=None)
                else:
                    me.follow.remove(user)
                    profile.followers.remove(request.user)
                return JsonResponse({
                        'status' : 'hecho', 'followers' : profile.followers.all().count(),
                        'id' : pk, 'type' : action, 'user' : user.username
                    }, safe=False)     
    try:
        me = Profile.objects.get(user = request.user)
    except:
        me = ''
    return render(request, 'usuarios/profile.html', {
        'profile' : profile, 'user' : user, 'me' : me, 
        'savedPost' :savedPost, 'posttagged' : postTagged,
        'form' : PostCreation(), 'formStory' : HistoryCreation(),
        'stories' : storyUser, 'posts' : post
    })

def edit_profile(request, pk):
    user = Profile.objects.get(id = pk)
    if user.user != request.user:
        return redirect('home')
    form = UserProfile(instance=user)
    if request.method == 'POST':
        form = UserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile/' + str(request.user.id))
        else:
            print(request.FILES)
            return redirect('home')
    return render(request, 'usuarios/edit_profile.html', {'form' : form})