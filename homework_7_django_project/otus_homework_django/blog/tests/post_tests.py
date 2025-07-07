import pytest

from blog.models import Post, Comment

@pytest.mark.django_db
def test_create_post(user_object):
	test_post = Post.objects.create(author=user_object, title='test title', text='test text')

	assert test_post.id is not None
	assert test_post.title == 'test title'
	assert test_post.text == 'test text'

@pytest.mark.django_db
def test_create_comment(user_object, post_object):
	test_comment = Comment.objects.create(author=user_object,  post=post_object, text='test text')

	assert test_comment.id is not None
	assert test_comment.text == 'test text'
