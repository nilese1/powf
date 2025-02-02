from typing import final

from django.views.generic import TemplateView


@final
class IndexView(TemplateView):
    template_name = 'landing/index.html'
