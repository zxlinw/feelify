from django.urls import path
from .views import EmotionPlaylistView

urlpatterns = [
    path('get-playlist/', EmotionPlaylistView.as_view(), name='get-playlist'),
]
