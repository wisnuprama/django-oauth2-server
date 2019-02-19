from django.urls import path

from apps.tokens.views import TokensView


urlpatterns = [
    path('tokens/', TokensView.as_view(), name='tokens'),
]