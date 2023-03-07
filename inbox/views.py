from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from django.contrib.auth.decorators import login_required
from usuarios.models import Profile
# Create yourviews here.


# Pagina de inicio del Inbox
def messanger(request):
    try:
        users = User.objects.all().exclude(username = request.user.username)
        profile = Profile.objects.get(user = request.user)
        # //== 'utils.py == // #
        chat_message = chat_users(request)
    except:
        users = {}
        chat_message = {} 
        profile = {}  

    return render(request, 'inbox/messanger.html', {
        'inbox' : True,
        'chat_message' : chat_message,
        'users' : users,
        'profile' : profile
    })


# Chat individual con el usuario
@login_required(login_url='login')
def displayMessanger(request, pk):
    users = Profile.objects.all().exclude(user = request.user)
    to_user = Profile.objects.get(id = pk)
    profile = Profile.objects.get(user = request.user)
    messages = Message.objects.filter(Q(sender = profile, received = to_user) | 
    Q(sender = to_user, received = profile)).order_by('-created')
    for message in messages:
        # if message.sender != profile:
        if message.received == profile:
                message.read = True
                message.save()

    # //== 'utils.py == // #
    chat_message = chat_users(request)

    return render(request, 'inbox/messanger.html', {
        'messages': messages,
        'chat_message' : chat_message,
        'to_user' : to_user,
        'users' : users,
        'profile' : profile
        })


#Mensajear con el usuario a partir de AJAX 
@csrf_exempt
def ajaxDisplay(request):
    to_user = request.POST.get('to_user')
    body = request.POST.get('body')

    received = Profile.objects.get(id = to_user)
    sender = Profile.objects.get(user = request.user)

    if sender == received:
        return JsonResponse({'status' : False}, safe=False)
    
    Message.objects.create(
        sender = sender,
        received = received,
        body = body
    )
    return JsonResponse({
        'body' : body,
        'imagen' : sender.avatar.url,
    }, safe=False)
   

# Emviar publicaciones a los usuarios
def send_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    post = Post.objects.get(id = pk)
    profile = Profile.objects.get (user = request.user)
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('user'))
        to_user = Profile.objects.get(user = user)
        Message.objects.create(
        sender = profile,
        received = to_user,
        postsended = post,
        )
        return redirect('messages-display', to_user.id)

    return render(request, 'inbox/sendpost.html', {'profile' : profile})


# Permite actualizar los nuevos mensajes que los usuarios reciben 
def newMessagesReceived(request):
    pk = request.GET.get('id')
    user = Profile.objects.get(id = pk)
    message = Message.objects.filter(sender = user).order_by('-created')[0]
    body = message.body
    imagen = message.sender.avatar.url
    return JsonResponse({'body' : body, 'imagen' : imagen, 'id' : message.id}, safe=False)


# DESPLEGAR LOS CHATS CON JQUERY(LO COMENTE PORQUE ES MUCHO CODIGO INNECESARIO)

# def displayMessanger(request):
#     id = request.GET.get('id')
#     to_user = User.objects.get(id = id)
#     messages = Message.objects.filter(Q(sender = request.user, received = to_user) | 
#     Q(sender = to_user, received = request.user)).order_by('-created')
#     from_user = request.user.username
#     messageFromChat = []
#     for message in messages:
#         messageFromChat.append( [{'users' : message.sender.username }, {'body' : message.body}])
#         if message.sender != request.user:
#             if message.received == request.user:
#                 message.read = True
#                 message.save()
        

#     return JsonResponse({
#         'to_user' : to_user.username,
#         'messageFromChat' : messageFromChat,
#         'from_user' : from_user,
#     }, safe=False)