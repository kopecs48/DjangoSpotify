from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home_page, name='home'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('recommendation/', views.recommendation_get, name='recommendation'),
    path('recommendationp/', views.recommendation_post, name='recommendationp'),
    path('liked/', views.liked_songs, name='liked_songs'),
    path('search/', views.search, name='search'),
    path('signup/' , views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('link/', views.link, name='link'),
    path('friends/', views.friends_list, name='friends'),
    path('sent_requests/', views.sent_requests, name='sent'),   # kinda dumb
    path('received_requests/', views.received_requests, name='received'),   # stupid
    path('results/add_liked_song/', views.add_song),    # This is tacky need to figure out alternative
    path('search/add_liked_song/', views.add_song),     # Tacky...
    path('add_liked_song/', views.add_song),    # Tacky...
    path('results/disliked_song/', views.dislike),    # This is tacky need to figure out alternative
    path('search/disliked_song/', views.dislike),     # Tacky...
    path('add_disliked_song/', views.dislike),    # Tacky...
    path('blog/', views.blog, name='blog'),
    path('create_blog/', views.create_blog, name='create_blog'), 
    path('delete/', views.delete_song, name='delete'),
    path('send_friend_request/<int:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:requestID>/', views.decline_friend_request, name='decline_friend_request'),
    path('remove_friend/<int:requestID>', views.remove_friend, name='remove_friend'),
    path('remove_request/<int:requestID>', views.remove_request, name='remove_request'),
    path('export/', views.export_liked, name="export"),
    path('recommendationp/add_liked_song/', views.add_song ),
    path('recommendationp/add_disliked_song/', views.dislike),
    re_path(r'^edit_comment/(?P<commentID>\d+)/', views.edit_profile_comment, name='edit_profile_comment'),

    re_path(r'^profile/(?P<user_name>\w+)/', views.profile, name='profile'),
    path('delete_profile_comment/<int:userID>/<int:prof_comment_id>/', views.delete_profile_comment, name='delete_profile_comment'),
    re_path(r'^delete_song_comment/(?P<songID>\w+)/(?P<song_comment_id>\w+)/', views.delete_song_comment, name='delete_song_comment'),
    re_path(r'^edit_song_comment/(?P<songID>\w+)/(?P<commentID>\w+)/', views.edit_song_comment, name='edit_song_comment'),
    re_path(r'^comments/(?P<song_id>\w+)/', views.comments, name='comments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)