from django.urls import path

from product.views import delete_all_products_view
from product.views import ProductCreateView
from product.views import ProductDeleteView
from product.views import ProductDetailView
from product.views import ProductImportView
from product.views import ProductListView
from product.views import ProductUpdateView
from product.views import SubscriberCreateView


app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('import/<str:task_id>/', ProductListView.as_view(), name='list'),
    path('import/', ProductImportView.as_view(), name='import'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('delete-all/', delete_all_products_view, name='delete-all'),
    path('create-webhook/', SubscriberCreateView.as_view(), name='create-hook'),
]
