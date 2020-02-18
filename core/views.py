from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.conf import settings

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        if settings.VUE_DEV:
            template_name = 'index_dev.html'
        else:
            template_name = "index_dj.html"
        return template_name
