import pytest
from django.urls import reverse
from blog.models import Post


@pytest.mark.django_db
def test_main_page_view(client, post_object):
    response = client.get(reverse("main-page"))

    assert response.status_code == 200
    assert post_object.title in response.content.decode()

@pytest.mark.django_db
def test_post_detail_view(client, post_object):
    url = reverse('post-detail', kwargs={'pk':post_object.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert post_object.title in response.content.decode()
    assert post_object.text in response.content.decode()


