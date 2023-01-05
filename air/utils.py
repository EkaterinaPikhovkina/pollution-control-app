from django.db.models import Count

from .models import *

menu = [{'title': "Ввід даних", 'url_name': 'add_data'},
        {'title': "Перегляд даних", 'url_name': 'show_data'},
        {'title': "Звіт", 'url_name': 'make_report'},
        {'title': "Новини", 'url_name': 'news'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        return context