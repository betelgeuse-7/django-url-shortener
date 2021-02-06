from django.urls import path

from .views import Index, Redirect

app_name = 'shorten'

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('r/<str:url>/', Redirect.as_view(), name="redirect"),
]
