import logging

from django.views.generic import ListView, DetailView

from .models import Post, Comment

logger = logging.getLogger(__name__)

class MainPage(ListView):
	model = Post
	paginate_by = 100
	ordering = ["-created_at"]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		logger.debug("MainPage context loaded with %d posts", len(context['object_list']))
		return context

class PostDetail(DetailView):
	model = Post
