from .models import Message
from django.db.models import Q
from usuarios.models import Profile

def chat_users(request):
    profile = Profile.objects.get(user = request.user)
    messages = Message.objects.filter(Q(received = profile)| Q(sender = profile)).order_by('-created')
    array = []
    newmessage = []
    
    for message in messages:
        if message.sender in array or message.received in array:
            continue
        elif message.received == profile:
            array.append(message.sender)
            newmessage.append(message)
        elif message.sender == profile:
                array.append(message.received)
                newmessage.append(message)

    return newmessage



    # for message in messages:
    #     if request.user == message.received:
    #         if message.sender in array:
    #             continue
    #         else:
    #             array.append(message.sender)
    #             newmessage.append(message)
    #     else:
    #         if request.user == message.sender:
    #             if message.received in array:
    #                 continue
    #             else:
    #                 array.append(message.received)
    #                 newmessage.append(message)