from django.urls import path

from .views import MainPage, PostDetail

urlpatterns = [
	path("", MainPage.as_view(), name = "main-page"),
	path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
]
