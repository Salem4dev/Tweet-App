from django import forms
from .models import Tweet

MAX_TWEET_LENGTH = 500

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']    

    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet too long.")
        return content
    