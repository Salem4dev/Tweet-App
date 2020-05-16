from rest_framework import serializers
from .models import Tweet
from django.conf import settings
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action.')
        return value 

class TweetCreateSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id','content', 'like']
    
    def get_like(self, obj):
        return obj.like.count()

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            print('value', value)
            raise serializers.ValidationError("This tweet too long.")
        return value

class TweetSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id','content', 'like', 'is_retweet', 'parent']
    
    def get_like(self, obj):
        return obj.like.count()
    
    # def get_content(self, obj):
    #     content = obj.content
    #     if obj.is_retweet:
    #         content = obj.parent.content
    #     return content
