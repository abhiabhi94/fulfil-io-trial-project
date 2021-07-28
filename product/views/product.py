import uuid

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.edit import FormView
from django_filters.views import FilterView
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin

from product.filters import ProductFilter
from product.forms import ProductForm
from product.forms import ProductImportForm
from product.models import Product
from product.tables import ProductTable
from product.tasks import import_products


class ProductImportView(FormView):
    form_class = ProductImportForm
    template_name = 'product/import.html'
    task = None

    def get_success_url(self):
        assert self.task is not None
        return reverse_lazy('product:list', args=[self.task.id])

    def form_valid(self, form):
        data = form.cleaned_data['product_file']
        with open('file' + str(uuid.uuid4()), 'wb') as fp:
            for chunks in data.chunks():
                fp.write(chunks)
        self.task = import_products.delay(fp.name)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.task is not None:
            context['task_id'] = self.task.task_id
        return context


class ProductListView(SingleTableMixin, FilterView):
    model = Product
    table_class = ProductTable
    template_name = 'product/list.html'
    paginate_by = 20
    paginator_class = LazyPaginator
    filterset_class = ProductFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['task_id'] = self.kwargs.get('task_id')
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    queryset = Product.objects.all()
    template_name = 'product/detail.html'


class ProductUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/form.html'
    success_message = 'The product %(name)s has been updated successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['update_view'] = True
        return context


class ProductDeleteView(SuccessMessageMixin, generic.DeleteView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product:list')
    template_name = 'product/confirm_delete.html'
    success_message = 'The product %(name)s has been deleted successfully.'


class ProductCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = 'product/form.html'
    form_class = ProductForm
    success_message = 'The product %(name)s has been created successfully.'


def delete_all_products_view(request, *args, **kwargs):
    request_method = request.method.lower()
    if request_method == 'get':
        return render(request, template_name='product/confirm_delete_all.html')

    elif request_method == 'post':
        Product.objects.delete_all()
        messages.success(request, _('All products have been deleted successfully.'))
        return redirect('product:import')

    return HttpResponseBadRequest
