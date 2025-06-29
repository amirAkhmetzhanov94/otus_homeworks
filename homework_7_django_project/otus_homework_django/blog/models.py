from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=100)
	text = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Author is {self.author} - {self.text}'

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)
	post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
	text = models.CharField(max_length=300)

	def __str__(self):
		return f'Comment by {self.author} on {self.post}'



