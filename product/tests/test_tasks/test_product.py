from unittest.mock import patch
import tempfile
import csv

from product.tasks import import_products


def test_import_products(faker):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as csvfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'sku', 'description'])
        writer.writeheader()
        rows = [{'name': faker.name(), 'sku': faker.slug(), 'description': faker.text()} for _ in range(100)]
        writer.writerows(rows)

        with patch('product.tasks.product.Product.objects.bulk_upsert') as mock_upsert:
            import_products(csvfile.name)

            assert mock_upsert.called_with(rows, keys=['sku'])
