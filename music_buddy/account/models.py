from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from music_buddy_app.models import *


class MyAccountManager(BaseUserManager):
	def create_user(self,username, password=None):
		# if not email:
		# 	raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			# email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			# email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60)
	username 				= models.CharField(max_length=30, unique=True)
	spotify_id 				= models.CharField(max_length=30, default="")
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)		
	friends_list			= models.ManyToManyField('self', blank=True, verbose_name="friends_list")
	image 					= models.ImageField(default='default.jpg', upload_to='profile_pics')
	liked_songs_total       = models.IntegerField(default=0)


	USERNAME_FIELD = 'username'
	# REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
	
	def update(self):
		super().save()
		img = Image.open(self.image.path) # Open image
        
        # resize image
		if img.height > 150 or img.width > 150:
			output_size = (150, 150)
			img.thumbnail(output_size) # Resize image
			img.save(self.image.path)

class Post(models.Model):
		title = models.CharField(max_length=255)
		author = models.ForeignKey(Account, on_delete=models.CASCADE)
		body = models.TextField()

		def __str__(self):
			return self.title + ' | ' + str(self.author)

class FriendRequest(models.Model):
	from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_user')
	to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_user')

class ProfileComment(models.Model):
	author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="commentor")
	webpage = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="profile")
	body = models.TextField(max_length=500)

	def __str__(self):
		return str(self.author) + ': ' + str(self.body)

class SongComment(models.Model):
	author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="authors")
	time = models.DateTimeField(auto_now_add=True)
	SongName = models.TextField(max_length=500)
	body = models.TextField(max_length=500)

	def __str__(self):
		return str(self.author) + ': ' + str(self.body)

