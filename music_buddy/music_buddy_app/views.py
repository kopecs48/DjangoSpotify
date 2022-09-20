import os
from django.http import JsonResponse
from requests import post
from .secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .forms import *
import spotipy
import spotipy.util as sp_util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from account.views import *
from account.forms import *
from account.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from pathlib import Path
import datetime
from django.db.models import F
# Used for basic search utilities it doesn't require redirect url or scope
client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

"""
This can be used if you want to save songs to your Spotify account
Potential problem: How to go about getting a new token if it expires

scope = 'user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private'
token = SpotifyOAuth( 
                     client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET, 
                     redirect_uri=REDIRECT_URI,
                     scope=scope,)
sp = spotipy.Spotify(token)
"""

# Home Page includes search functionality
def home_page(request):
    form = SearchForm()
    popular_today = todays_hits()
    popular_global = top_global()
    return render(request, 'home.html', {'form': form, 'today': popular_today, 'global': popular_global})

# Home page gets really clunky with the top songs
def search(request):
    songs = []
    form = SearchForm(request.POST)
    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        results = sp.search(q=search_query, limit=12)
        res = list(results['tracks']['items'])
        x = 0
        while x < len(res):
            song_id = res[x]['id']
            songs.append({'id': song_id})
            x += 1
        return render(request, 'search_results.html', {'form': form, 'albums': songs})
    else:
        return render(request, 'search_results.html', {'form': form})

def leaderboard(request):
    users = Account.objects.all().order_by("-liked_songs_total")
    return render(request, 'leaderboard.html', {'users': users})

#for intial page
def recommendation_get(request):
    form = RecommendForm()
    return render(request, 'recommendation.html', {'form': form})

#for form retreival and posting albums
def recommendation_post(request):
    form = RecommendForm(request.POST)
    genres= [request.POST['genre']]
    songs = []
    list = []
    if form.is_valid():
        try:
            auth_manager = createAuthManager(request)
            sp_new = spotipy.Spotify(auth_manager=auth_manager)
            test = request.POST['history']
            rTracks = sp_new.current_user_recently_played(limit=4)
            for track in rTracks['items']:
                list.append(track['track']['uri'])
            
        except:
            rTracks = None
        

        results = sp.recommendations(country='US', seed_genres=genres, seed_tracks=list,
                                    limit=20,
                                    target_energy=request.POST['energy'],
                                    target_acousticness=request.POST['acousticness'],
                                    target_danceability=request.POST['danceability'], 
                                    target_liveliness=request.POST['liveliness'])
                                             
        for track in results['tracks']:
            songs.append({'id' : track['id']})

        return render(request, 'recommendation.html', {'form': form, 'albums': songs})
    else:
        return render(request, 'recommendation.html', {'form': form})

def liked_songs(request):
    if request.user.is_authenticated:
        liked_songs = LikedSongs.objects.filter(user=request.user).values_list('song_id', flat=True)        
        songs = list()    
        for id in liked_songs:
            songs.append(id)
        return render(request, 'liked_songs.html', {'items': songs})
    return render(request, 'liked_songs.html')

# Display 5 songs from the "Today's Top Hits" playlist
def todays_hits():
    song_list = []
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
    target_playlist = sp.playlist(playlist_id = playlist_id)
    for x in range(len(target_playlist['tracks']['items'])):
        song_list.append({'id': target_playlist['tracks']['items'][x]['track']['id']})
    random.shuffle(song_list)
    res = list(song_list)[:5]
    return res
    
# Display 5 songs from the "Top Songs - Global" playlist
def top_global():
    song_list = []
    playlist_id = '37i9dQZEVXbNG2KDcFcKOF'
    target_playlist = sp.playlist(playlist_id = playlist_id)
    for x in range(len(target_playlist['tracks']['items'])):
        song_list.append({'id': target_playlist['tracks']['items'][x]['track']['id']})
    random.shuffle(song_list)
    res = list(song_list)[:5]
    
    return res

@login_required
def link(request):
    cache_path = ".cache"
    if request.user.is_authenticated:
        username = request.user.username
        cache_path += "-" + str(username)

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private user-read-recently-played',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
                            

    if request.GET.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.GET.get("code"))
        sp = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private user-read-recently-played',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
        return redirect('/')



    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
    
        return redirect(auth_url)


def createAuthManager(request):
    cache_path = ".cache"
    if request.user.is_authenticated:
        username = request.user.username
        cache_path += "-" + str(username)

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private user-read-recently-played',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
                            

    if request.GET.get("code"):
        auth_manager.get_access_token(request.GET.get("code"))
        # Step 3. Being redirected from Spotify auth page
        sp = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private user-read-recently-played',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
        

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
    
        return redirect(auth_url)

    return auth_manager

def blog(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {"posts": posts})   

# Song details/comments page
def comments(request, song_id):
        song = song_id
        track = sp.track(song)
        artists = []
        release_date = track['album']['release_date']
        for artist in track['artists']:
            artists.append(artist['name'])
        name = sp.track(song)['name']
        likes = LikedSongs.objects.filter(song_id = song).count()
        dislikes = dislikedSong.objects.filter(song_id = song).count()
        total = likes + dislikes
        color = "#F84F31"
        percent = "0"
        if total != 0:
            percent = str(int((likes/(likes + dislikes))*100))
            color = "#F84F31"

        if request.method == 'POST':
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                body = request.POST.get('body', '')
                author = request.user
                time = datetime.datetime.now()
                SongName = song
                SongComment.objects.create(author = author,  time = time, SongName= SongName , body = body)
            return redirect('comments' , song)
            #return HttpResponseRedirect(request.path_info)

        post = SongComment.objects.all()
        form = CreateSongCommentForm()
        return render(request, 'comments.html', { 'song': song, 'form': form,  'post': post, 'name': name, 'likes':likes, 'dislikes':dislikes, 'percent':percent +"%", 'color':color, 'total':total , 'artists': artists, 'release_date': release_date})
    
# Add song to Liked Songs
def add_song(request):
    if request.user.is_authenticated:
        value = request.GET.get('song_id')
        query = LikedSongs.objects.filter(song_id=value, user=request.user).all()
        Account.objects.filter(username=request.user).update(liked_songs_total=F('liked_songs_total') + 1)
        dislikedSong.objects.filter(song_id=value, user = request.user).delete()
        for x in query:
            if x.song_id == value:
                response = JsonResponse({"error": "Song is already liked, song is not added"}, safe=False)
                response.status_code = 403
                return response
        store_song = LikedSongs()
        store_song.user = request.user
        store_song.song_id = value
        store_song.save()
        return HttpResponse(200)
    response = JsonResponse({"error": "You need to be logged in to use this function"}, safe=False)
    response.status_code = 403
    return response

# Add song to disliked Songs
def dislike(request):
    if request.user.is_authenticated:
        value = request.GET.get('song_id')
        query = dislikedSong.objects.filter(song_id=value).all()
        LikedSongs.objects.filter(song_id=value, user = request.user).delete()
        for x in query:
            if x.song_id == value:
                response = JsonResponse({"error": "This song is already disliked"})
                response.status_code = 403 
                return response
        store_song = dislikedSong()
        store_song.user = request.user
        store_song.song_id = value
        store_song.save()
    return HttpResponse(200)

def delete_song(request):
    if request.user.is_authenticated:
        form = SelectionForm(request.POST)
        if request.method == 'POST':
            song_id = request.POST.getlist('selection')
            if len(song_id) == 0:
                return redirect('liked_songs')
            for item in song_id:
                song_id = LikedSongs.objects.filter(user=request.user).get(song_id=item)
                song_id.delete()
    return redirect('liked_songs')

"""
Need to fix later

TODO:
- Create Friends/Users Search Functionality
"""
def friends_list(request):
    names = FriendRequest.objects.all()
    my_friends = Account.objects.filter(username=request.user).all().values('friends_list')

    # Get current friends
    f_list = list()
    for friend in my_friends:
        if friend['friends_list'] is not None:
            curr_id = friend['friends_list']
            f_list.append(Account.objects.get(id=curr_id))

    # Get list of all users of site that are not in your friends list
    all_names = Account.objects.all()
    all_users = list()
    for name in all_names:
        if name not in f_list and name != request.user:
            all_users.append(name)

    return render(request, 'friends_list.html', {'all_users': all_users, 'curr_friends': f_list})

def sent_requests(request):
    outgoing = FriendRequest.objects.filter(from_user=request.user).all()
    outgoing_list = list()
    for name in outgoing:
        outgoing_list.append(name)
    return render(request, 'sent_requests.html', {'outgoing_req': outgoing_list})

def received_requests(request):
    pending = FriendRequest.objects.filter(to_user=request.user).all()
    pending_list = list()
    for name in pending:
        pending_list.append(name)
    return render(request, 'received_requests.html', {'incoming_req': pending_list})


def profile(request, user_name):
    current_profile = Account.objects.get(username=user_name)
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=current_profile)
        if p_form.is_valid():
            user = p_form.save()
            user.update()
            
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            body = request.POST.get('body', '')
            webpage = current_profile
            author = request.user
            ProfileComment.objects.create(author = author,webpage = webpage, body = body)
        return redirect('profile', current_profile)

    form = CreateCommentForm()
    p_form = ProfileUpdateForm(instance=request.user)
    posts = ProfileComment.objects.filter(webpage = current_profile)
    cache_path = ".cache"
    username = current_profile.__str__
    cache_path += "-" + str(user_name)
    path = Path(cache_path)

    song_list = []
    liked_songs = LikedSongs.objects.filter(user=current_profile).values_list('song_id', flat=True)
    
    if len(liked_songs) >= 5:
        recent = liked_songs[len(liked_songs)-5:len(liked_songs)]
    else:
        recent = liked_songs[len(liked_songs)-len(liked_songs):len(liked_songs)]
  
    for liked in recent:
        song_list.append({'name' : sp.track(liked)['name'], 'id': sp.track(liked)['id']})
        
    song_list.reverse()
   
    if path.is_file():
        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
        sp_new = spotipy.Spotify(auth_manager=auth_manager)
        
        
        playlists = sp_new.current_user_playlists()
        temp = []
        for p in playlists['items']:
            temp.append({'id': p['id'], 'name': p['name']})
        return render(request, 'profile.html', {'friend': current_profile, 'playlists': temp, 'form': form, 'p_form': p_form, 'posts': posts , 'liked_songs': song_list})
        
    else:
        return render(request, 'profile.html', {'friend': current_profile, 'form': form, 'p_form': p_form, 'posts': posts, 'liked_songs': song_list})


def delete_profile_comment(request, userID, prof_comment_id):
    user = Account.objects.get(pk=userID)
    target_post = ProfileComment.objects.get(pk=prof_comment_id)
    target_post.delete()    
    return redirect('profile', user.username)

def delete_song_comment(request, songID, song_comment_id):
    target_post = SongComment.objects.get(pk=song_comment_id)
    target_post.delete()    
    return redirect('comments', songID)
    
# Save songs from Liked Songs page to your Spotify Account
def export_liked(request):
    # spaghetti code, fix later
    found = False
    pl_name = "MusicBuddy Playlist"
    pl_desc = "Playlist of songs from Liked Songs page from MusicBuddy"    
    cache_path = ".cache"
    cache_path += "-" + str(request.user)
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read playlist-read-private user-library-modify playlist-modify-public playlist-modify-private',
                                            cache_handler=cache_handler, 
                                            show_dialog=True,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    form = SelectionForm(request.POST)    
    if request.method == 'POST':
        song_id = request.POST.getlist('selection')
        if len(song_id) == 0:
            return redirect('liked_songs')
        user_id = sp.me()['id']        
        playlists = sp.user_playlists(user=user_id)
        target_playlist = ''
        if len(playlists['items']) == 0:
            target_playlist = sp.user_playlist_create(user=user_id, public=True, name=pl_name, description=pl_desc)
            target_playlist = target_playlist['id']
        else:
            for x in range(len(playlists['items'])):
                if pl_name in playlists['items'][x]['name']:
                    target_playlist = playlists['items'][x]['id']
                    found = True
                    break
            if found is False:
                target_playlist = sp.user_playlist_create(user=user_id, public=True, name=pl_name, description=pl_desc)
                target_playlist = target_playlist['id'] 
        songs_in_pl = sp.playlist_items(playlist_id=target_playlist, limit=None)
        for x in range(len(songs_in_pl['items'])):
            current_id = songs_in_pl['items'][x]['track']['id']
            if current_id in song_id:
                song_id.remove(current_id)
        if len(song_id) != 0:
            sp.playlist_add_items(playlist_id=target_playlist, items=song_id)
    return redirect('liked_songs')