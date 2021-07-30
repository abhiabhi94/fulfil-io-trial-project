from http import HTTPStatus as status
from django.urls import reverse_lazy
from django.contrib import messages
import pytest
from pytest_django.asserts import assertTemplateUsed

from product.models import Subscriber



@pytest.mark.django_db
def test_creating_webhook(client):
    url = reverse_lazy('product:create-hook')
    data = {'url': 'http://example.com', 'event': Subscriber.Event.PRODUCT_CREATED.value}

    response = client.post(url, data=data, follow=True)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'hook/form.html')
