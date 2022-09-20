from django.db import models
from account.models import Account


# Create your models here.
class Musicdata(models.Model):
    acousticness = models.FloatField()
    artists = models.TextField()
    danceability = models.FloatField()
    duration_ms = models.FloatField()
    energy = models.FloatField()
    explicit = models.FloatField()
    id = models.TextField(primary_key=True)
    instrumentalness = models.FloatField()
    key = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    name = models.TextField()
    popularity = models.FloatField()
    release_date = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()        
    year = models.IntegerField()

class LikedSongs(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    song_id = models.TextField()

class dislikedSong(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    song_id = models.TextField()