from django.urls import include
from django.urls import path


urlpatterns = [
    path('products/', include('product.urls')),
    path('task-progress/', include('celery_progress.urls')),
]
