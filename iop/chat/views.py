from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import json

from .models import Conversation, Message
from news.models import Articles

@login_required
@require_POST
def delete_conversation(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    conv.delete()
    return redirect('chat_inbox')

@login_required
def inbox(request):
    conversations = request.user.conversations.prefetch_related('participants', 'messages').all()
    
    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conv.other_user = conv.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/inbox.html', {'conversations': conversations})

@login_required
def conversation(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    
    conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    other_user = conv.participants.exclude(id=request.user.id).first()
    messages = conv.messages.all()

    return render(request, 'chat/conversation.html', {
        'conv': conv,
        'messages': messages,
        'other_user': other_user,
    })

@login_required
@require_POST
def send_message(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    data = json.loads(request.body)
    body = data.get('body', '').strip()

    if not body:
        return JsonResponse({'error': 'Pusta wiadomość.'}, status=400)

    msg = Message.objects.create(conversation=conv, sender=request.user, body=body)

    return JsonResponse({
        'id': msg.id,
        'body': msg.body,
        'created_at': msg.created_at.strftime('%H:%M'),
        'sender': request.user.username,
    })

@login_required
def start_conversation(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    seller = article.autor

    if seller == request.user:
        return redirect('news_detail', pk=article_id)

    conv = Conversation.objects.filter(
        participants=request.user,
        article=article
    ).filter(participants=seller).first()

    if not conv:
        conv = Conversation.objects.create(article=article)
        conv.participants.add(request.user, seller)
        Message.objects.create(
            conversation=conv,
            sender=request.user,
            body=f'Cześć, jestem zainteresowany/a ogłoszeniem: {article.title}'
        )

    return redirect('chat_conversation', conv_id=conv.id)

@login_required
def get_messages(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    last_id = request.GET.get('last_id', 0)
    msgs = conv.messages.filter(id__gt=last_id)
    msgs.exclude(sender=request.user).update(is_read=True)

    return JsonResponse({'messages': [
        {
            'id': m.id,
            'body': m.body,
            'created_at': m.created_at.strftime('%H:%M'),
            'sender': m.sender.username,
            'is_mine': m.sender == request.user,
        } for m in msgs
    ]})