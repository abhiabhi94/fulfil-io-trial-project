import os

import numpy
import pandas
from celery.utils.log import get_task_logger
from celery_progress.backend import ProgressRecorder
from django.utils.translation import gettext_lazy as _

from config import celery_app
from product.models import Product


logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def import_products(self, filepath):
    def get_objects(dataframes):
        objects = []
        for line_count, row in dataframes.iterrows():
            objects.append(Product(**{
                'name': row['name'],
                'sku': row['sku'],
                'description': row['description'],
                'is_active': True if line_count % 2 == 0 else False
            }))
        return objects

    try:
        progress_recorder = ProgressRecorder(self)

        data_frame = pandas.read_csv(filepath)
        total_lines = data_frame.shape[0]
        data_frame.drop_duplicates(subset=['sku'], keep='last', inplace=True)

        chunk_count = 25
        for num, chunk in enumerate(numpy.array_split(data_frame, chunk_count)):
            Product.objects.bulk_upsert(objects=get_objects(chunk), keys=['sku'])
            progress_recorder.set_progress(
                chunk.shape[0] * (num + 1),
                total=total_lines,
                description=_('Products processed')
            )

    finally:
        # remove the processed file
        os.remove(filepath)
