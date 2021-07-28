from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from product.forms import SubscriberForm


class SubscriberCreateView(generic.CreateView):
    form_class = SubscriberForm
    template_name = 'hook/form.html'
    success_url = reverse_lazy('product:create-hook')

    def form_valid(self, form):
        messages.success(self.request, _('Webhook created successfully.'))
        return super().form_valid(form)
