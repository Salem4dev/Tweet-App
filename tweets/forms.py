from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 200

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']    

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            print('content', content)
            raise forms.ValidationError("This tweet too long.")
        return content
    