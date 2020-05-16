from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Tweet
User = get_user_model()
from rest_framework.test import APIClient
# Create your tests here.
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='123')
        self.user_ahmed = User.objects.create_user(username='ahmed-abc2', password='1234')
        Tweet.objects.create(content='1', user=self.user)
        Tweet.objects.create(content='2', user=self.user)
        Tweet.objects.create(content='3', user=self.user)
        Tweet.objects.create(content='4', user=self.user_ahmed)
        self.count = Tweet.objects.all().count()
    
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='5', user=self.user)
        tweet_id = Tweet.objects.get(content='5', user=self.user)
        self.assertEqual(tweet_obj.id, tweet_id.id)
        self.assertEqual(tweet_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='123')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_tweet_action_like(self):
        client = self.get_client()
        tweet_obj = Tweet.objects.get(content='3', user=self.user)
        response = client.post('/api/tweets/action/', {'id': tweet_obj.id, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('like')
        self.assertEqual(like_count, 1)
        print(response.json())

    def test_tweet_action_unlike(self):
        client = self.get_client()
        tweet_obj = Tweet.objects.get(content='3', user=self.user)
        response = client.post('/api/tweets/action/', {'id': tweet_obj.id, 'action': 'like'})
        response = client.post('/api/tweets/action/', {'id': tweet_obj.id, 'action': 'unlike'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('like')
        self.assertEqual(like_count, 0)
        print(response.json())
    
    def test_tweet_action_retweet(self):
        client = self.get_client()
        count = self.count
        tweet_obj = Tweet.objects.get(content='3', user=self.user)
        response = client.post('/api/tweets/action/', {'id': tweet_obj.id, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(14, new_tweet_id)
        new_count = Tweet.objects.all().count()
        self.assertEqual(count + 1, new_count)

    
    def test_tweet_create_api_view(self):
        request_data = {'content': 'This is a test create api view'}
        client = self.get_client()
        tweet_id = Tweet.objects.filter(user=self.user).last()
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        self.assertNotEqual(tweet_id.id, new_tweet_id)
        new_count = Tweet.objects.all().count()
        self.assertEqual(self.count + 1, new_count)
    
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        check_tweet_id = Tweet.objects.filter(user=self.user).last()
        response = client.get(f'/api/tweets/{check_tweet_id.id}/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        tweet_id = response_data.get('id')
        self.assertNotEqual(tweet_id, check_tweet_id)
    
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        check_tweet_id = Tweet.objects.filter(user=self.user).first()
        url = f'/api/tweets/{check_tweet_id}/delete/'
        print('url', url)
        response = client.delete(''.format(url))
        self.assertEqual(response.status_code, 200)
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)
        # user2_tweet_id = Tweet.objects.filter(user=self.user_ahmed).first()
        # url2 = f'/api/tweets/{user2_tweet_id}/delete/'
        # print('url2', url)
        # response_incorrect_user = client.delete(''.format(url2))
        # self.assertEqual(response_incorrect_user.status_code, 401)

        
