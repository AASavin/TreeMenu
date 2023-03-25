from django.views.generic import TemplateView


class TestPageView(TemplateView):
    template_name = 'app_menu/test_page.html'

