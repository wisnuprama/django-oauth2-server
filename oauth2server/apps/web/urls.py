from django.urls import path

from apps.web.views import AuthorizeView


urlpatterns = [
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
]