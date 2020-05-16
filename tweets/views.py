from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tweet
import random
from .forms import TweetForm
from .serlializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer,
)
ALLOWED_HOSTS = settings.ALLOWED_HOSTS
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
# Create your views here.
def home_view(request, *arg, **kwargs):
    # return HttpResponse('Hello World!')
    return render(request, 'pages/home.html', context={}, status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def createTweetView(request, *arg, **kwargs):
    data = request.POST
    serializer = TweetCreateSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        # serializer.save(user=request.user, status=201)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *arg, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *arg, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)
    

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *arg, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    new_qs = qs.filter(user=request.user)
    if not new_qs.exists():
        return Response({'message': 'You can not delete tweet which belong to another USER.'}, status=401)
    obj = new_qs.first()
    obj.delete()
    return Response({'message': 'Tweet has been delete'}, status=200)
    
    # return HttpResponse(f"<h1>hello {tweet_id} - content {obj.content}")
    # return JsonResponse(data, status=status) # json.dumps content_type='application/json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *arg, **kwargs):
    print(request.POST, request.data)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.like.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.like.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            new_tweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)
    
    # return HttpResponse(f"<h1>hello {tweet_id} - content {obj.content}")
    return JsonResponse(data, status=status) # json.dumps content_type='application/json

def createTweetView_PureDjango(request, *arg, **kwargs):
    if not request.user.is_authenticated:
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    print('request.ajax', request.is_ajax())
    print('form.is_valid', form.is_valid())
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        print('form.errors', form.errors)
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/forms.html', context={'form': form})

def tweet_list_view_puredjango(request, *arg, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {'response': tweet_list}
    return JsonResponse(data, status=200)

def tweet_detail_view_puredjango(request, tweet_id, *arg, **kwargs):
    data = {
        'id': tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json
