from django.urls import path, include

urlpatterns = [
    path('api/v1/', include(('apps.tokens.urls', 'tokens'), namespace='api_v1')),
    path('web/', include(('apps.web.urls', 'web'), namespace='web')),
]