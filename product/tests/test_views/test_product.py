import csv
import tempfile
import os
from http import HTTPStatus as status

from django.urls import reverse_lazy
import pytest
from pytest_django.asserts import assertTemplateUsed

from product.models import Product


@pytest.mark.django_db
def test_product_creation(faker, client):
    url = reverse_lazy('product:create')
    data = {'name': faker.name(), 'sku': faker.slug(), 'description': faker.text()}

    response = client.post(url, data, follow=True)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/detail.html')


@pytest.mark.django_db
def test_product_create_get_request(client):
    url = reverse_lazy('product:create')

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/form.html')


@pytest.mark.django_db
def test_product_details(product, client):
    url = reverse_lazy('product:detail', args=[product.pk])

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/detail.html')
    assert response.context['product'] == product


@pytest.mark.django_db
def test_product_listing(product, client):
    url = reverse_lazy('product:list')

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/list.html')
    assert response.context['object_list'] == [product]
    assert response.context['table'] is not None
    assert response.context['filter'] is not None
    assert response.context['paginator'] is not None


@pytest.mark.django_db
def test_product_update_get_request(product, client):
    url = reverse_lazy('product:update', args=[product.pk])

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/form.html')
    assert response.context['product'] == product


@pytest.mark.django_db
def test_product_updation(product, client, faker):
    url = reverse_lazy('product:update', args=[product.pk])

    response = client.post(url, data={'name': faker.name()}, follow=True)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/form.html')
    assert response.context['product'] == product
    assert response.context['update_view'] is True


@pytest.mark.django_db
def test_product_delete_get_request(product, client):
    url = reverse_lazy('product:delete', args=[product.pk])

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/confirm_delete.html')
    assert response.context['product'] == product


@pytest.mark.django_db
def test_product_deletion(product, client):
    url = reverse_lazy('product:delete', args=[product.pk])

    response = client.post(url, follow=True)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/list.html')


@pytest.mark.django_db
def test_delete_all_products_get_request(client):
    url = reverse_lazy('product:delete-all')

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/confirm_delete_all.html')


@pytest.mark.django_db
def test_delete_all_products(client, django_assert_num_queries):
    url = reverse_lazy('product:delete-all')
    products = [Product(name=f'product {i}', description='description {i}', sku=f's-k-u {i}') for i in range(100)]
    Product.objects.bulk_upsert(products, keys=['sku'])

    with django_assert_num_queries(5):  # some queries are made to save the next ID(checkpoint)
        response = client.post(url, follow=True)

        assert response.status_code == status.OK
        assertTemplateUsed(response, 'product/import.html')


@pytest.mark.django_db
def test_non_get_or_post_request_to_delete(client):
    url = reverse_lazy('product:delete-all')

    response = client.delete(url)

    assert response.status_code == status.BAD_REQUEST


@pytest.mark.django_db
def test_import_product_get_request_without_task_id(client):
    url = reverse_lazy('product:import')

    response = client.get(url)

    assert response.status_code == status.OK
    assertTemplateUsed(response, 'product/import.html')
    assert response.context.get('task_id') is None


@pytest.mark.django_db
def test_import_product(client, faker):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as csvfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'sku', 'description'])
        writer.writeheader()
        rows = [{'name': faker.name(), 'sku': faker.slug(), 'description': faker.text()} for _ in range(100)]
        writer.writerows(rows)
    url = reverse_lazy('product:import')

    try:
        with open(csvfile.name, 'rb') as csvfile:
            response = client.post(url, data={'product_file': csvfile}, follow=True)

            assert response.status_code == status.OK
            assertTemplateUsed(response, 'product/import_progress.html')
            assert response.context['task_id'] is not None
    finally:
        os.remove(csvfile.name)

