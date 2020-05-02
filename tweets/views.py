from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
import random
from .forms import TweetForm
ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request, *arg, **kwargs):
    # return HttpResponse('Hello World!')
    return render(request, 'pages/home.html', context={}, status=200)

def createTweetView(request, *arg, **kwargs):
    # return HttpResponse('Hello World!')
    form = TweetForm(request.POST or None)
    print('request.ajax', request.is_ajax())
    print('form.is_valid', form.is_valid())
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
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

def tweet_list_view(request, *arg, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {'response': tweet_list}
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *arg, **kwargs):
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
    
    # return HttpResponse(f"<h1>hello {tweet_id} - content {obj.content}")
    return JsonResponse(data, status=status) # json.dumps content_type='application/json
