from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse 
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from inbox.models import Message
from usuarios.models import Profile
from .models import Post, SavePost, Comment, Histories, Notifications, Likes
from .forms import PostCreation, HistoryCreation
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


# Create your views here.


# PAGINA DE INICIO
def home(request):
    # print(profile.follow.all())
    histories = Histories.objects.all()
    for x in histories:
        if timezone.now() > x.expired and x.permanent == False:
            x.delete()
    
    try:
        followers = Profile.objects.get(user = request.user)
        followers = followers.follow.all()
        profile = Profile.objects.get(user = request.user)
        savedpost = SavePost.objects.filter(user = request.user)
        likepost = Likes.objects.filter(user = request.user)
        notifications = Message.objects.filter(received = profile, read = False).count()
        activity = Notifications.objects.filter(user = request.user, see = False).count()
        if not savedpost:
            postsaved = []
        else:
            postsaved = []
            for x in savedpost:
                postsaved.append(x.post)

        if not likepost:
            postliked = []
        else:
            postliked = []
            for x in likepost:
                postliked.append(x.post)
                
    except:
        postsaved = []
        postliked = []
        profile = []
        notifications = {}
        followers = []
        activity = 0

    return render(request, 'core/home.html', {
        'notifications' : notifications, 'posts' :Post.objects.all(),
        'savedpost' : postsaved, 'followers' : followers, 'form' : PostCreation(),
        'profile' : profile, 'histories' : histories,
        'users' : Profile.objects.all(), 'formStory' : HistoryCreation(), 
        'notifi' : activity, 'likepost' : postliked,
        })




@csrf_exempt
def save_post(request):
    id = request.POST.get('id')
    type = request.POST.get('type')
    post = Post.objects.get(id = id)
    if type == 'guardar':
        SavePost.objects.create(
            post = post,
            user = request.user
        )
        return JsonResponse({'type' : type, 'id' : id }, safe=False)
    else:
        SavePost.objects.get(post = post, user = request.user).delete()
        return JsonResponse({'type' : type, 'id' : id}, safe=False)


@csrf_exempt
def like_post(request):
    id = request.POST.get('id')
    type = request.POST.get('type')
    post = Post.objects.get(id = id)
    if type == 'like':
        Likes.objects.create(
            post = post,
            user = request.user
        )
        post.like += 1
        post.save()
        return JsonResponse({'type' : type, 'id' : id }, safe=False)
    else:
        Likes.objects.get(post = post, user = request.user).delete()
        post.like -= 1
        post.save()
        return JsonResponse({'type' : type, 'id' : id}, safe=False)




@login_required(login_url='login')
def createPost(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        taggeded = request.POST.getlist('tagged')
        description = request.POST.get('description')
        post = Post.objects.create(
            imagen = imagen,
            host = profile,
            description = description
        )
        for x in taggeded:
            user = User.objects.get(id = x)
            post.tagged.add(user)
        return redirect('home')
    else:
        return redirect('profile')


# Crear historias
@login_required(login_url='login')
def CreateHistory(request):
    profile = Profile.objects.get(user = request.user)
    formStory = HistoryCreation()
    if request.method == 'POST':
        form = HistoryCreation(request.POST, request.FILES)
        if form.is_valid():
            h = form.save(commit=False)
            h.user = profile
            h.expired = timezone.now() + timedelta(hours=21)
            h.save()

            return redirect('home')
        else:
            return redirect('createHistory')
            
    return render(request, 'core/create-histories.html', {'form': form})


# Mostrar historias
def historyJson(request):
    pk = request.GET.get('id')
    profile = Profile.objects.get(id = pk)
    x = Histories.objects.filter(user = profile)
    historiesImg = []
    historiesDes = []
    historiesUser = []
    historiesTimes = []
    for y in x:
        historiesImg.append(y.history.url)
        historiesDes.append(y.description)
        historiesUser.append(y.user.name)
        historiesTimes.append(y.created.strftime("%a, %b a las %I:%M %p"))

    return JsonResponse({
        'historiesImg': historiesImg, 'historiesDes': historiesDes,
        'historiesUser': historiesUser, 'historiesTimes' : historiesTimes,
        }, safe=False)


# Mostrar la publicacion de un usuario
def postUser(request, pk):
    post = Post.objects.get(id = pk)
    save_post = SavePost.objects.filter(user = request.user, post = post)
    like_post = Likes.objects.filter(user = request.user, post = post)
    comments = Comment.objects.filter(postcomments = post)
    return render(request, 'core/post.html', {
        'post': post, 'comments': comments,
        'saved' : save_post, 'liked' : like_post,
        })



@csrf_exempt
def createComment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status' : 'mal'}, safe = False)
    profile = Profile.objects.get(user = request.user)
    id = request.POST.get('id')
    post = Post.objects.get(id = id)
    comment = request.POST.get('comment')
    if not comment:
        return
    x = Comment.objects.create(
        user = profile,
        postcomments = post,
        name = comment
    )
    return JsonResponse({
        'comment' : comment, 'host': request.user.username, 'pk': x.id,
        'avatar' : profile.avatar.url,
        }, safe=False)

def deleteComment(request):
    id = request.GET.get('id')
    comment = Comment.objects.get(id = id)
    if request.user == comment.user.user:
        comment.delete()
        return JsonResponse({}, safe=False)


# Notificaciones de los usuarios
@login_required(login_url='login')
def notifications_user(request, pk):
    user = User.objects.get(id = pk)
    if request.user != user:
        return redirect('home')
    profile = Profile.objects.get(user = user)
    notifications = Notifications.objects.filter(user = user).order_by('-created')
    for x in notifications:
        x.see = True
        x.save()
    return render(request, 'core/notifications.html', {'noti': notifications, 'profile' : profile})