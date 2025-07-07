import pytest

from django.contrib.auth.models import User

from blog.models import Post


@pytest.fixture(scope='session', autouse=True)
def django_db_setup():
	pass

@pytest.fixture
def user_object():
	user = User.objects.create(username='test')
	return user

@pytest.fixture
def post_object(user_object):
	post = Post.objects.create(author=user_object, title = 'test post', text='test post')
	return post

