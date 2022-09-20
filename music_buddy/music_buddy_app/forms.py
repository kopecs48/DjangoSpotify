from django import forms
import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'size': 100,
                                                                 'style': 'font-size: 23px'
                                                                 }))

#Profile for User
class Profile(AuthenticationForm):
    username =  forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=150, required=True)

#Recommendations Form

# iterable
GENRE_CHOICES =(
    ("alt-rock", "ALT-ROCK"),
    ("alternative", "ALTERNATIVE"),
    ("blues", "BLUES"),
    ("club", "CLUB"),
    ("classical", "CLASSICAL"),
    ("country", "COUNTRY"),
    ("disco", "DISCO"),
    ("edm", "EDM"),
    ("hip-hop", "HIP-HOP"),
    ("metal", "METAL"),
    ("rock", "ROCK"),
    ("reggae", "REGGAE"),
    ("pop", "POP"),
    ("soul", "SOUL")

)

CUSTOM_CHOICES =(
    ("0.1", "MIN"),
    ("0.25", "LOW"),
    ("0.5", "MEDIUM"),
    ("0.75", "HIGH"),
    ("0.9", "MAX")
)

class RecommendForm(forms.Form):
    genre = forms.ChoiceField(choices = GENRE_CHOICES )
    acousticness = forms.ChoiceField(choices = CUSTOM_CHOICES )
    danceability = forms.ChoiceField(choices = CUSTOM_CHOICES )
    energy = forms.ChoiceField(choices = CUSTOM_CHOICES )
    liveliness = forms.ChoiceField(choices = CUSTOM_CHOICES )
    history = forms.BooleanField(required = False)

# Used for Exporting Liked Songs to Spotify or Deleting the Songs off of the Liked Songs List
class SelectionForm(forms.Form):
    selection = forms.BooleanField(required=False)
